using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheScalableWebhook
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheScalableWebhookStack(app, "TheScalableWebhookStack");
            app.Synth();
        }
    }
}
