function PlaidLink() 
{
    var self = this;

    self.environment;
    self.linkToken;
    self.accessToken;

    self.products = function () 
    {
        // update this list manually
        let transactions = ['Transactions'];
        return transactions;
    }

    self.isNullOrEmpty = function (text) 
    {
        return (!text || text.length === 0);
    }

    self.showPlaidLink = async function () 
    {
        const fetchLinkToken = async () => 
        {
            const response = await fetch('/api/create_link_token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(self.products()),
            });
            const responseJSON = await response.json();
            return responseJSON.link_token;
        };

        const configs =
        {
            // Required, fetch a link token from your server and pass it
            // back to your app to initialize Link.
            token: await fetchLinkToken(),
            onLoad: function () 
            {
                // Optional, called when Link loads
            },
            onSuccess: async function (public_token, metadata) 
            {
                // Send the public_token to your app server.
                const response = await fetch("/api/set_access_token", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(public_token)
                });
                const responseJSON = await response.json();
                self.accessToken = responseJSON.access_token;

                // Establish Link with Logged in User
                await fetch("/home/establish_item", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(self.accessToken)
                });
            },
            onExit: function (err, metadata)
            {
                // The user exited the Link flow.
                if (err != null)
                {
                    // The user encountered a Plaid API error prior to exiting.
                }
                // metadata contains information about the institution
                // that the user selected and the most recent API request IDs.
                // Storing this information can be helpful for support.
            },
            onEvent: function (eventName, metadata)
            {
                // Optionally capture Link flow events, streamed through
                // this callback as your users connect an Item to Plaid.
                // For example:
                // eventName = "TRANSITION_VIEW"
                // metadata  = {
                //   link_session_id: "123-abc",
                //   mfa_type:        "questions",
                //   timestamp:       "2017-09-14T14:42:19.350Z",
                //   view_name:       "MFA",
                // }
            }
        };

        const handler = Plaid.create(configs);
        handler.open();
    }

    //self.refreshToken = async function () 
    //{
    //    const response = await fetch('/home/getupdatetoken', {
    //        method: 'POST',
    //        headers: {
    //            'Content-Type': 'application/json'
    //        },
    //        body: JSON.stringify(self.accessToken()),
    //    });
    //    const responseJSON = await response.json();
    //    var handler = Plaid.create({
    //        token: responseJSON.link_token,
    //        onLoad: function ()
    //        {
    //            // Optional, called when Link loads
    //        },
    //        onSuccess: function (public_token, metadata)
    //        {
    //            console.log("refresh token success!");
    //        },
    //        onExit: function (err, metadata)
    //        {
    //            // The user exited the Link flow.
    //            if (err != null)
    //            {
    //                // The user encountered a Plaid API error prior to exiting.
    //            }
    //            // metadata contains information about the institution
    //            // that the user selected and the most recent API request IDs.
    //            // Storing this information can be helpful for support.
    //        },
    //        onEvent: function (eventName, metadata)
    //        {
    //            // Optionally capture Link flow events, streamed through
    //            // this callback as your users connect an Item to Plaid.
    //            // For example:
    //            // eventName = "TRANSITION_VIEW"
    //            // metadata  = {
    //            //   link_session_id: "123-abc",
    //            //   mfa_type:        "questions",
    //            //   timestamp:       "2017-09-14T14:42:19.350Z",
    //            //   view_name:       "MFA",
    //            // }
    //        }
    //    });
    //    handler.open();
    //}
};