readarray -t patterns < <(jq -r '.[] | keys | .[]' info.json);
for pattern in "${patterns[@]}"
do
   cd $pattern/python;
   if test -f "requirements.txt"; then
     python3 -m venv .env;
     source .env/bin/activate;
     pip3 install -r requirements.txt;
     readarray -t stacks < <(npx -q cdk ls);
     for stack in "${stacks[@]}"
       do
          echo "npx cdk synth $stack";
          npx cdk synth "$stack";
       done    
     deactivate
   fi
   cd ../../;
done
