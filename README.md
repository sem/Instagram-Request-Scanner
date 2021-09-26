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
Since it's recommended to start your count when your requests are below 200, there is an option to automatically approve all your pending follow requests. All pending requests will be accepted **only in the first run**. 
By changing ```accept``` to ```True``` in line 624, all your pending follow requests will be accepted. If it's set to ```False```, it will just directly move on to counting your incoming requests. Note that none of the followers that get accepted will be appended to the JSON. If you've already had a first run, but wish to accept followers again; simply delete ```first_run.json```.

```py
if __name__ == "__main__":
    '''
    To accept requests set Scraper(accept=True)

    Will only accept the first run to make sure your requests are below 200
    '''
    Scraper(accept=False)
```

> In this example, ```Scraper``` is set to ```False```, so none of the current pending follow requests will be accepted.

### Interval
The standard interval between each run will be randomized between 2400 and 3000 seconds. It will be shortened as you get more requests, since you can only get to see the 200 most recent users that requested a follow. By shortening the interval, you can avoid letting new requests get past 200, so your count will stay accurate. <br/>

```py
if self.new_requests >= 50:
    self.waiting = random.randint(2400, 3000)
                    
if self.new_requests >= 100:
    self.waiting = random.randint(1800, 2400)

if self.new_requests >= 150:
    self.waiting = random.randint(900, 1200)
```

> Once your run has finished and the amount of new received requests is below 50, the standard interval will be used.

### Messages
Since the code has to be running somewhere 24 hours a day in order to get an accurate amount, it might be frustrating if you have to go to your console every time to look at your total amount of requests. Therefore, each run a message will be sent to your Instagram account which will include the total amount of the pending follow requests, the date, username, etc.

<img src="https://user-images.githubusercontent.com/78478073/134776231-c03d1b82-dbaf-4a94-8767-a98de3450ae4.png" width="330"> <img src="https://user-images.githubusercontent.com/78478073/134776317-24d32298-fa68-4b5b-94de-557a8ea1bb8b.png" width="330">

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
At the beginning, you will be asked to log in with your Instagram account. Your username and password will be encrypted and stored in ```secrets.pickle```, so you don't have to manually log in every time the script runs.  There will also be a ```sessions``` folder created to have the messages sent to your account. Once you're logged in, it will automatically get your pending follow requests and a countdown for the next run will be displayed.

<img src="https://user-images.githubusercontent.com/78478073/134772574-fcc1a33a-5956-402c-8797-e13984699d3d.png" width="330"> <img src="https://user-images.githubusercontent.com/78478073/134772621-4a31e48a-9c14-4bbc-989a-e170642d49e3.png" width="330"> <img src="https://user-images.githubusercontent.com/78478073/134784244-8a06f079-52ea-46a8-9199-6eeffc227079.png" width="330">

> As you can see, your follow requests will be shown past the 200 or 1000 limit while the browser version of Instagram still shows 200. <br/>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
sem@moolenschot.nl <br/>
[Reddit](https://www.reddit.com/user/moolenschot) <br/>
[Instagram](https://www.instagram.com/semmoolenschot)

## License
Distributed under the MIT License. See ```LICENSE``` for more information.
