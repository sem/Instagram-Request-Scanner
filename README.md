![Title](https://user-images.githubusercontent.com/78478073/134777257-84f9a70d-9253-4342-be34-3c632400b69c.png)

## Table of Contents
- [About the project](#about-the-project)
  * [Disadventages](#disadventages)
  * [Accepting follow requests](#accepting-follow-requests)
  * [Interval](#interval)
  * [Messages](#messages)
- [Getting started](#getting-started)
  * [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## About the project
Instagram stops displaying new incoming following requests once it reaches a thousand users. Even though you will still get the follow requests, they will not show you the exact amount anymore. Instagram never publicly announced why, but the most likely reason for this is, so the larger private accounts will not take advantage of this. Without this limit, owners of these accounts can clickbait thousands of people into requesting a follow without showing them any content at all. The official Instagram app on IOS or Android will show a maximum amount of 1000 pending follow requests, but on the browser version just 200. There is only one solution to count past these limits, and that is by storing a count of the 200 recent requests in a loop, and appending new incoming follow requests to that count.

### Disadventages
- One disadvantage is that the script **requires to be running 24 hours a day** to keep track of new incoming follow requests. Therefore, there has to be a decent amount of logins per day to make this work, but it's dependent on how many new follow requests your account gets. While Instagram has never publicly announced how many times you can log in per day, the script will try its best to avoid your account getting any type of punishment. The interval between every run (login) will be based on the number of requests it got in the previous run. <br/>

- Another disadvantage is that you have to **start with less than 200 pending follow requests**, to have an accurate count. Otherwise, it will only take the 200 most recent requests and start from there.

### Accepting follow requests
Since it's recommended to start your count when your requests are below 200, there is an option to automatically approve all your pending follow requests. For each run, 200 users will be accepted until your pending requests are below the 200 limit. Once it's below 200, a file named ```accept.json``` will be created, so no more requests will be accepted when appending them to your total amount in ```username_pending_users.json```. Note that none of the users that get accepted will be appended to that JSON; only the users that request a follow after accepting is finished will be appended to the count. If you have already accepted followers, but wish to accept again, then you can delete ```accept.json```. 
By changing ```accept``` to ```True``` at line 631, all your pending follow requests will be accepted. If it's set to ```False```, it will just directly move on to counting your incoming requests. 

> ```py
> if __name__ == "__main__":
>     '''
>     To accept follow requests -> Scraper(accept=True)
> 
>     Will accept every run until your follow requests are below 200
>     Can only accept a maximum amount of 200 requested users per run
>     '''
>     Scraper(accept=False)
> ```
>
> In this example, ```Scraper``` is set to ```False```, so none of the current pending follow requests will be accepted.

### Interval
The standard interval between each run will be randomized between 2400 and 3000 seconds. It will be shortened as you get more requests, since you can only get to see the 200 most recent users that requested a follow. By shortening the interval, you can avoid letting new requests get past 200, so your count will stay accurate. <br/>

> ```py
> if self.new_requests >= 50:
>     self.waiting = random.randint(2400, 3000)
>                     
> if self.new_requests >= 100:
>     self.waiting = random.randint(1800, 2400)
> 
> if self.new_requests >= 150:
>     self.waiting = random.randint(900, 1200)
> ```
>
> Once your run has finished and the amount of new received requests is below 50, the standard interval will be used.

### Messages
Since the code has to be hosted somewhere to get an accurate count, it won't make it easy to access your console very quickly to look at your total amount of requests. That's why a message will be sent to your account at each run which will include the amount of requests, the current date, etc.

> <p align="center">
> <img width="1551" alt="134870026-cb4d7ad8-b749-4773-a7e7-d66af4a3c72c" src="https://user-images.githubusercontent.com/78478073/134982788-16ad44e3-0a28-44e8-856a-6434bcab5245.png">
> <img width="1552" alt="Screenshot 2021-09-30 at 15 51 49" src="https://user-images.githubusercontent.com/78478073/135468401-b02bed41-fdb0-4c64-88e0-31fc9a259353.png">
> </p>
> You will also be notified when your account is still accepting follow requests

## Getting started
### Installation 
1. Clone the repository.
```
https://github.com/semmoolenschot/Instagram-Request-Scanner.git
```
2. Install the requirements.
```
pip install -r requirements.txt
```

## Usage
At the beginning, you will be asked to log in with your Instagram account. Your username and password will be encrypted and stored in ```secrets.pickle``` so you don't have to manually log in every time the script runs.  There will also be a ```sessions``` folder created which will also include your credentials encrypted with the same key as ```secrets.pickle``` . The ```sessions``` folder is required to log in with the API, so the messages with your data can be sent to your account. Once you're logged in, it will automatically get your pending follow requests and a countdown for the next run will be displayed.

> <p align="center">
>  <img width="1552" alt="Screenshot 2021-09-27 at 10 08 54" src="https://user-images.githubusercontent.com/78478073/134871453-ba531feb-e996-4a9e-a0ac-246a3974dacc.png">
> <img width="686" alt="Screenshot 2021-09-27 at 21 54 16" src="https://user-images.githubusercontent.com/78478073/134976017-f6401906-b254-4ce6-8d70-876d4fba549c.png">
> </p>
>
> As you can see, your follow requests will be shown past 200 while the browser version of Instagram still only show 200 requests. <br/>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
sem@moolenschot.nl <br/>
[Reddit](https://www.reddit.com/user/moolenschot) <br/>
[Instagram](https://www.instagram.com/semmoolenschot)

## License
Distributed under the MIT License. See ```LICENSE``` for more information.
