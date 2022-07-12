package main

import (
	"bytes"
	"encoding/json"
	"html/template"
	"log"
	"net/http"
	"os"
)

var toppage = `<html>
  <head>
  </head>
  <body>
    <p>
      Well, hello there!
    </p>
    <p>
      We're going to now talk to the GitHub API. Ready?
      <a href="https://github.com/login/oauth/authorize?scope=user:email&client_id={{.}}">Click here</a> to begin!
    </p>
    <p>
      If that link doesn't work, remember to provide your own <a href="/apps/building-oauth-apps/authorizing-oauth-apps/">Client ID</a>!
    </p>
  </body>
</html>
`

var (
	CLIENT_ID     = os.Getenv("CLIENT_ID")
	CLIENT_SECRET = os.Getenv("CLIENT_SECRET")
	OAUTH_URL     = "https://github.com/login/oauth/access_token"
)

type OauthPostField struct {
	ClientId     string `json:"client_id"`
	ClientSecret string `json:"client_secret"`
	Code         string `json:"code"`
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		tmpl, err := template.New("top").Parse(toppage)
		if err != nil {
			log.Println(err)
		}
		tmpl.Execute(w, CLIENT_ID)
	})
	mux.HandleFunc("/callback", func(w http.ResponseWriter, r *http.Request) {
		v := r.URL.Query()
		code := v.Get("code")
		p := OauthPostField{CLIENT_ID, CLIENT_SECRET, code}
		d, err := json.Marshal(&p)
		if err != nil {
			log.Println(err)
		}
		body := bytes.NewBuffer(d)
		log.Println("body:", body)
		req, err := http.NewRequest("POST", OAUTH_URL, body)
		if err != nil {
			log.Println(err)
			return
		}
		req.Header.Add("Content-Type", "application/json")
		req.Header.Add("Accept", "application/json")
		client := new(http.Client)
		res, err := client.Do(req)
		if err != nil {
			log.Println(err)
			return
		}
		log.Println(res.StatusCode)
		buf := make([]byte, 4096)
		defer res.Body.Close()
		n, _ := res.Body.Read(buf)
		log.Println("---response---")
		log.Println(string(buf[0:n]))

	})
	log.Fatal(http.ListenAndServe(":8080", mux))

}
