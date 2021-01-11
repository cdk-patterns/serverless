set -e
readarray -t arr < <(jq -r '.[] | keys | .[]' info.json);
for i in "${arr[@]}"
do
   cd $i/typescript;
   npm i;
   npm run build;
   npm run test;
   cd ../../;
done