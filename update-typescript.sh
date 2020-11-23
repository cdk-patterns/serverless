set -e
readarray -t arr < <(jq -r '.[] | keys | .[]' info.json);
for i in "${arr[@]}"
do
   cd $i/typescript;
   rm -rf node_modules
   npx npm-check-updates -u
   echo "$i updated"
   cd ../../;
done