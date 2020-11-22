function getCDKVersion() {
    version="1.60.0"
    
    readarray -t requirements <<<"$(<requirements.txt)"
     for requirement in "${requirements[@]}"
       do
          if [[ "$requirement" == aws-cdk.* ]]; then
            IFS='==' read -a fields <<<"$requirement"
            version=${fields[2]}
            break;
          fi
       done
       
    echo $version
}

readarray -t patterns < <(jq -r '.[] | keys | .[]' info.json);
for pattern in "${patterns[@]}"
do
   cd $pattern/python;
   if test -f "requirements.txt"; then
     #we want to build with the version of cdk defined in requirements.txt
     version=$(getCDKVersion)
     python3 -m venv .env;
     source .env/bin/activate;
     pip3 install -r requirements.txt;
     readarray -t stacks < <(npx -q cdk@${version} ls)
     if [[ "${#stacks[@]}" == 0 ]]; then
       exit 1
     fi
     for stack in "${stacks[@]}"
       do
          echo "npx cdk synth $stack";
          npx cdk@${version} synth "$stack";
       done    
     deactivate
   fi
   cd ../../;
done
