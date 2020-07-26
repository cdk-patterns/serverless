/*
  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

// You can send up to 10 events to Amazon EventBridge simulataneously.

module.exports.params = {
  Entries: [ 
    {
      // Event envelope fields
      Source: 'custom.myATMapp',
      EventBusName: 'default',
      DetailType: 'transaction',
      Time: new Date(),

      // Main event body
      Detail: JSON.stringify({
        action: 'withdrawal',
        location: 'MA-BOS-01',
        amount: 300,
        result: 'approved',
        transactionId: '123456',
        cardPresent: true,
        partnerBank: 'Example Bank',
        remainingFunds: 722.34
      })
    },
    {
      // Event envelope fields
      Source: 'custom.myATMapp',
      EventBusName: 'default',
      DetailType: 'transaction',
      Time: new Date(),

      // Main event body
      Detail: JSON.stringify({
        action: 'withdrawal',
        location: 'NY-NYC-001',
        amount: 20,
        result: 'approved',
        transactionId: '123457',
        cardPresent: true,
        partnerBank: 'Example Bank',
        remainingFunds: 212.52
      })
    },
    {
      // Event envelope fields
      Source: 'custom.myATMapp',
      EventBusName: 'default',
      DetailType: 'transaction',
      Time: new Date(),

      // Main event body
      Detail: JSON.stringify({
        action: 'withdrawal',
        location: 'NY-NYC-002',
        amount: 60,
        result: 'denied',
        transactionId: '123458',
        cardPresent: true,
        remainingFunds: 5.77
      })
    }    
  ]
}