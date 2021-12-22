CHECK=$(for file in $(find . -name '*.py' -not -path './gooddata-*-client/*' -path './gooddata*/gooddata*' -exec echo {} \;); do
    echo $file : $(head -n 1 $file)
done | grep -vi "Gooddata Corporation")
if [[ ! -z "$CHECK" ]]
then
    echo "Following files do not start with copyright header: \n $CHECK"
    exit 1
fi
echo "Copyrights ok"
