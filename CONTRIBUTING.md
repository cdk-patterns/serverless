# How To Contribute
This repo is designed to be a collection of aws serverless architecture patterns built with cdk. That means it should
eventually hold a cdk version of all patterns presented by AWS heros. If you want to contribute that is amazing and I will work through the process with you.

There are three different types of contribution today:
1. A brand new pattern
2. Add a new language implementation for an existing pattern
3. Converting Lambda Fns to CDK Language

## Adding a Brand New Pattern
This is where you have an implementation you want to share with the world that isn't currently in the codebase. Alternatively you may have seen someone talk about a pattern somewhere and you want to code it yourself to learn but not waste the code.

**Note** All patterns need to be in at least TypeScript and Python before I announce them but you can contribute the pattern in any CDK supported language and I will port it to Python/TS then announce

Contribution Steps:

1. Find a pattern that you want to share
2. Open an issue on this repo stating that you want to add this pattern so other people don't duplicate effort. Include links to arch pics in the issue
3. Branch the repo into your own personal github account
4. Build your pattern, make sure you add unit tests and a useful level of documentation including a simple arch diagram. If possible please try and link the pattern to the AWS Well Architected Framework in the readme and link to external sources for more info. Please also make sure you credit the original creator of the pattern, this is not about stealing content.
5. If it is TypeScript, make sure your pattern has the npm run deploy task added
6. Open up a pull request and start the merge discussion!

## Adding a new language for an existing pattern
Today all patterns are in TypeScript/Python with some in .Net and Java. If you want to add any supported CDK language for any pattern my only ask is keep it the exact same logically as the TypeScript version (usually the base reference). Also try not to be super opinionated about the implementation itself, I try to keep my personal opinions out of the patterns so that when engineers pick one up for the first time there is no cognitive burden working out my coding style.

Contribution Steps:

1. Open an issue stating what you want to do
2. Branch the repo into your own personal github account
3. Add your new language implementation
4. Open up a pr

## Converting Lambda Fns to CDK Language
This would be a big help and is a great way to get started contributing. When a pattern launches typically I build it in TypeScript and then port it over to Python. In order to reduce bugs at launch I typically reuse the JS Lambda Fn in the Python version then slowly refactor over time to full Python. If you spot one of these JS functions in a Python pattern and want to convert it to Python it is small enough that you could just do it and open a Pull Request
