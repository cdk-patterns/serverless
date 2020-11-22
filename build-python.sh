readarray -t patterns < <(jq -r '.[] | keys | .[]' info.json);
for pattern in "${patterns[@]}"
do
   cd $pattern/python;
   if test -f "requirements.txt"; then
     python3 -m venv .env;
     source .env/bin/activate;
     pip3 install -r requirements.txt;
     readarray -t stacks < <(npx -q cdk@1.74.0 ls);
     if [[ "${#stacks[@]}" == 0 ]]; then
       exit 1
     fi
     for stack in "${stacks[@]}"
       do
          echo "npx cdk synth $stack";
          npx cdk@1.74.0 synth "$stack";
       done    
     deactivate
   fi
   cd ../../;
done
