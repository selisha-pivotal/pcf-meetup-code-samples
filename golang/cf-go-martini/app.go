package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"

	"github.com/go-martini/martini"
	"github.com/joefitzgerald/cfenv"
	"github.com/martini-contrib/render"
)

type myData struct {
	Metadata string
	Payload  string
}

func main() {
	m := martini.Classic()

	db := initDB()

	m.Use(DB(db))
	m.Use(render.Renderer())

	m.Get("/get", func(r render.Render, db *sql.DB) {
		languages, err := fetchLanguages(db)

		if err != nil {
			r.HTML(500, "error", err)
		} else {
			r.HTML(200, "languages", languages)
		}
	})

	m.Get("/ver", func(r render.Render) {
		appEnv := cfenv.Current()
		r.HTML(200, "version", appEnv)
	})

	m.Get("/wipe", func(r render.Render, db *sql.DB) {

		wipeData(db)

		r.JSON(200, "OK")
	})

	m.Get("/set/:data", func(params martini.Params, r render.Render, db *sql.DB) {
		mydata := params["data"]

		insertData(db, mydata)

		r.JSON(200, "OK")
	})

	//    m.Post("/data/:resource", binding.Json( attribute{} ), func(attr attribute, params martini.Params, writer http.ResponseWriter)
	//		resource :=  ( params["resource"] )
	//    	writer.Header().Set("Content-Type", "application/json")
	//
	//  		return http.StatusOK, "POST placeholder " + resource
	//    })

	m.Run()
}

func fetchLanguages(db *sql.DB) (myDataStruct []*myData, err error) {
	rs, err := db.Query("select metadata, payload FROM val_store")
	if err != nil {
		return nil, err
	}
	defer rs.Close()
	fmt.Println("Fetch Query run  \n")

	myDataStruct = make([]*myData, 0)

	fmt.Println("Starting DB fetch /n")
	for rs.Next() {
		fmt.Println("Fetch row . . . . /n")
		tmpMyData := new(myData)
		err = rs.Scan(&tmpMyData.Metadata, &tmpMyData.Payload)
		myDataStruct = append(myDataStruct, tmpMyData)

		if err != nil {
			return nil, err
		}
	}
	err = rs.Err()
	if err != nil {
		return nil, err
	}

	return
}

func DB(db *sql.DB) martini.Handler {
	return func(c martini.Context) {
		c.Map(db)
		c.Next()
	}
}

func initDB() *sql.DB {
	db, err := sql.Open("mysql", dsn())
	if err != nil {
		panic(err.Error())
	}

	db.SetMaxOpenConns(4) // for ClearDB free plan

	fmt.Println("Ping DB  \n")

	err = db.Ping()
	if err != nil {
		panic(err.Error())
	}

	fmt.Println("Schema created ?	 \n")
	if schemaIsNotCreated(db) {
		createSchema(db)
	}

	return db
}

func dsn() string {
	services := cfenv.Current().Services
	var mysqlService cfenv.Service

	for _, instances := range services {
		for _, instance := range instances {
			if contains(instance.Tags, "mysql") {
				mysqlService = instance
				fmt.Println("Found DB service broker ==> mysql\n")
			}
		}
	}

	credentials := mysqlService.Credentials
	return fmt.Sprintf("%v:%v@tcp(%v:3306)/%v",
		credentials["username"],
		credentials["password"],
		credentials["hostname"],
		credentials["name"])
}

func schemaIsNotCreated(db *sql.DB) bool {
	rs, err := db.Query("select * from val_store limit 1")
	//	rs, err := db.Query("drop table val_store")
	if err != nil {
		fmt.Println("Schema is not created\n")
		return true
	} else {
		fmt.Println("Schema is created\n")
		rs.Close()
		return false
	}
}

func createSchema(db *sql.DB) {
	_, err := db.Exec(
		"CREATE TABLE val_store (metadata varchar(100), payload varchar(150)) ENGINE=InnoDB DEFAULT CHARSET=utf8")

	if err != nil {
		panic(err.Error())
	}
	fmt.Println("Created Schema\n")

	tx, err := db.Begin()
	if err != nil {
		panic(err.Error())
	}

	insertRow(db, "INSERT INTO val_store (metadata, payload) VALUES ('Test', 'Test')")

	err = tx.Commit()
	if err != nil {
		panic(err.Error())
	}
}

func wipeData(db *sql.DB) {
	db.Query("delete from val_store")
}

func insertData(db *sql.DB, data string) {

	if len(data) > 0 {
		sql_var := fmt.Sprintf("INSERT INTO val_store (metadata, payload) VALUES ('%s' , '%s')", data, data)
		fmt.Printf(sql_var)
		insertRow(db, sql_var)
	}
}

func insertRow(db *sql.DB, query string) {
	_, err := db.Exec(query)
	if err != nil {
		panic(err.Error())
	}
}

func contains(s []string, e string) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}
