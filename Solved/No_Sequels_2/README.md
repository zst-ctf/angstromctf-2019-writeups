# No Sequels 2
Web

## Challenge 

This is the sequel to No Sequels. You'll see the challenge page once you solve the first one.

Author: SirIan

## Solution

After solving No Sequels, we see this page with a source code.

	Here's your first flag: actf{no_sql_doesn't_mean_no_vuln}
	Access granted, however suspicious activity detected. Please enter password for user 'admin' again, but there will be no database query.
	Enter Password:
	[____________]

	router.post('/site', verifyJwt, function (req, res) {
	    // req.user is assigned from verifyJwt
	    if (!req.user.authenticated || !req.body.pass2) {
	        res.send("bad");
	    }
	 
	    var query = {
	        username: req.user.name,
	    }
	 
	    var db = req.db;
	    db.collection('users').findOne(query, function (err, user) {
	        console.log(user);
	        if (!user){
	            res.render('access', {username:' \''+req.user.name+'\' ', message:"Only user 'admin' can log in with this form!"});
	        }
	        var pass = user.password;
	        var message = "";
	        if (pass === req.body.pass2){
	            res.render('final');
	        } else {
	            res.render('access', {username:' \''+req.user.name+'\' ', message:"Wrong LOL!"});
	        }
	 
	    });
	 
	});

From the code, it seems we need to extract the password from No Sequel 1.

- https://blog.0daylabs.com/2016/09/05/mongo-db-password-extraction-mmactf-100/

Extract it using regex and bruteforcing.

	$ python3 solve.py 
	>> Progress: c
	>> Progress: co
	>> Progress: con
	>> Progress: cong
	>> Progress: congr
	>> Progress: congra
	>> Progress: congrat
	...
	>> Progress: congratsyouwi
	>> Progress: congratsyouwin
	>> Progress: congratsyouwin$

Submit `congratsyouwin` and we get the final flag

	Here's your final flag: actf{still_no_sql_in_the_sequel}

## Flag

	actf{still_no_sql_in_the_sequel}
