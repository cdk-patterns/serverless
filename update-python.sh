readarray -t patterns < <(jq -r '.[] | keys | .[]' info.json);

pythonPackage=aws-cdk.core;
version=$(curl -Ls https://pypi.org/pypi/$pythonPackage/json | jq -r .info.version)
echo "latest version is $version"

for pattern in "${patterns[@]}"
do
   cd $pattern/python;
   if test -f "requirements.txt"; then
     echo "updating $pattern"
     #initialize empty array for new requirements
     updatedReqs=()
     readarray -t requirements <<<"$(<requirements.txt)"
     for requirement in "${requirements[@]}"
       do
          if [[ "$requirement" == aws-cdk.* ]]; then
            IFS='==' read -a fields <<<"$requirement"
            updatedReqs+=("${fields[0]}==$version")
          else updatedReqs+=("$requirement")
          fi
       done
     var=$( IFS=$'\n'; echo "${updatedReqs[*]}" )
     echo "$var" >| requirements.txt
   fi
   cd ../../;
done