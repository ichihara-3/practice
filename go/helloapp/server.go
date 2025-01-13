package main

import (
    "net/http"

    "github.com/jmoiron/sqlx"
    "github.com/labstack/echo/v4"
    _ "github.com/go-sql-driver/mysql"
)



type greetings struct {
	Id int  `db:"id"`
	Message string `db:"message"`
}

type GreetingResponse struct {
    Message string `json:"message"`
}

var (
    con *sqlx.DB
)

func main() {
    e := echo.New()

    con, err := sqlx.Open("mysql", "myuser:mypassword@tcp(db:3306)/mydb")
    if err != nil {
        e.Logger.Fatal(err)
    }
    defer con.Close()
    e.GET("/", GetHandler)
    e.Logger.Fatal(e.Start(":8080"))
}

func GetHandler(c echo.Context) error {
    var row greetings
    err := con.Get(&row, "SELECT * FROM greetings ORDER BY RAND() LIMIT 1")
    if err != nil {
        c.Logger().Error(err)
        return c.JSON(http.StatusInternalServerError, GreetingResponse{Message: "Internal Server Error"})
    }
    return c.JSON(http.StatusOK, GreetingResponse{Message: row.Message})
}