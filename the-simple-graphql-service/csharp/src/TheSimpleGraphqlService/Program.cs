using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheSimpleGraphqlService
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheSimpleGraphqlServiceStack(app, "TheSimpleGraphqlServiceStack");
            app.Synth();
        }
    }
}
