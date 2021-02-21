using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Polly
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new PollyStack(app, "PollyStack");
            app.Synth();
        }
    }
}
