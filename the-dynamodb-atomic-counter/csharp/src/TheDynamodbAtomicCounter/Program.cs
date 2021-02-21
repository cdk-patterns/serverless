using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheDynamodbAtomicCounter
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheDynamodbAtomicCounterStack(app, "TheDynamodbAtomicCounterStack");
            app.Synth();
        }
    }
}
