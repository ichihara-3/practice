find ~/repos/nst/JSONTestSuite/test_parsing -name 'y*' |while read json; do cat ${json} | python3 parser.py 1>/dev/null; if [ $? -eq 1 ]; then echo ${json};fi ; done
find ~/repos/nst/JSONTestSuite/test_parsing -name 'n*' |while read json; do cat ${json} | python3 parser.py 2>/dev/null; if [ $? -eq 0 ]; then echo ${json};fi ; done


