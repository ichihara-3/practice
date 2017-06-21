zip := System args at(1)
url := URL with("http://www.post.japanpost.jp/cgi-zip/zipcode.php?zip=#{zip}&x=76&y=8" interpolate)

data := url fetch

data print
