
# The Lambda Trilogy

This is a CDK project containing 3 different stacks representing the 3 states of lambda

- Single Purpose Function
- Fat Lambda
- Lambda-lith

## Extra Setup

To deploy this project successfully you do need to install the dependencies for the lambda-lith.
This is because it uses Flask to route the different URLs and a WSGI compatibility library to make 
it work inside a lambda. 

I did originally use virtualenv but then found this [issue](https://github.com/aws/aws-cdk/issues/5484) so when
presented with the option of creating a lambda layer or just doing the basics, I chose the basics.

I tried to make this as simple as possible. 

From a terminal
```shell
cd lambdas/the_lambda_lith
pip install -r requirements.txt --target flask


```
## Standard Setup

After you have completed the Extra Setup steps above you can from the root directory follow these standard setup instructions

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
