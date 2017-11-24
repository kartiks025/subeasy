//#include <simplecpp>
#include <bits/stdc++.h> //directly include all std packages of gcc/C++
using namespace std;

class Tweet
{
	int tweet_id;
	int parent_tweet
	int user_id;
	std::vector<int> tweet_reply_id;
	string tweet;

public:
	Tweet(int &tweet_id, int &user_id, string &text, int &parent_tweet){
		this->tweet_id = tweet_id;
		this->user_id = user_id;
		this->tweet = text;
		this->parent_tweet = parent_tweet;
	};
	// ~Tweet();
	Tweet(const Tweet &p) : 
    tweet_id(p.tweet_id),
    parent_tweet(p.parent_tweet),
    user_id(p.user_id),
    tweet(p.tweet),
    tweet_reply_id(p.tweet_reply_id)
    {
    };
	string getTweetText(){
		return tweet;
	}
	int getTweetUser(){
		return user_id;
	}
	void addreply(int id){
		tweet_reply_id.push_back(id);
		return;
	}

	vector<int>* replyVector(){
		return &tweet_reply_id;
	} 
	
};

class User
{
	int user_id;
	string username;
	std::vector<int> tweet_posted_ids;
	std::vector<int> followed_ids;
public:
	User(int &user_id, string &username){
		this->user_id = user_id;
		this->username = username;
	};
	User(const User &p) : 
    user_id(p.user_id),
    username(p.username),
    tweet_posted_ids(p.tweet_posted_ids),
    followed_ids(p.followed_ids)
    {
    };

	string getuserName(){
		return username;
	}
	// ~User();
	void addFollower(int &follow_id){
		bool alreadyfollower = false;
		for(size_t i = 0; i < followed_ids.size();i++){
			if (followed_ids[i] == follow_id){
				alreadyfollower = true;
				break;}
		}
		if (alreadyfollower){
			cout<<"UserID "<<user_id<<" is already following UserID "<<follow_id<<"\n";
		}
		else {
			int follow_copy = follow_id;
			this->followed_ids.push_back(follow_copy);
			cout<<"UserID "<<user_id<<" has started following UserID "<<follow_id<<"\n";
		}
		return;
	}
	
	void removeFollower(int &follow_id){
		bool alreadyfollower = false;
		size_t i;
		for(i = 0; i < followed_ids.size();i++){
			if (followed_ids[i] == follow_id){
				alreadyfollower = true;
				break;}
		}
		if (alreadyfollower){
			followed_ids.erase(followed_ids.begin()+i);
			cout<<"UserID "<<user_id<<" has unfollowed UserID "<<follow_id<<"\n";
		}
		else {
			cout<<"UserID "<<user_id<<" is not following UserID "<<follow_id<<"\n";
		}
		return;
	}
	void getFollow(){
		sort(followed_ids.begin(),followed_ids.end());
		for(size_t i = 0; i < followed_ids.size();i++){
			cout<<followed_ids[i]<<" ";
		}	
		cout<<"\n";
		return;
	}

	void addTweet(int &tweetId){
		tweet_posted_ids.push_back(tweetId);
		return;
	}

	vector<int>* tweetVector(){
		return &tweet_posted_ids;
	} 

	vector<int>* followVector(){
		return &followed_ids;
	} 
};



class Network
{
	std::vector<User> users;
	std::vector<Tweet> tweets;
	int num_users;
	int num_tweets;

public:
	Network(){
		num_users = 0;
		num_tweets = 0;

	};
	// ~Network();
	void addUser(string &name){
		num_users++;
		User newUser(num_users,name);
		users.push_back(newUser);
		cout<<"User "<<name<<" added. User ID: "<<num_users<<"\n";
	}

	int totalusers(){
		return num_users;
	}
	User* getuser(int id){
		return &users[id-1];
	}

	void printUsers(){
		for (size_t i = 0; i < users.size(); ++i)
		{
			cout<<i+1<<" "<<users[i].getuserName()<<"\n";
					}
		return;
	}

	void addTweet(int &userId, string &tweettext){
		if(userId>num_users || userId<=0){
			cout<<"UserID "<<userId<<" does not exist\n";
		}
		else{
			num_tweets++;
			int parent = -1;
			Tweet newTweet(num_tweets,userId,tweettext,parent);
			tweets.push_back(newTweet);
			users[userId-1].addTweet(num_tweets);
			cout<<"UserID "<<userId<<" tweeted "<<tweettext<<"\n";
		}
		return;
	}
	int totaltweet(){
		return num_tweets;
	}
	void printFollowersTweet(int uid)
	{
		vector<int> *v = users[uid-1].followVector();
		vector<int> alltweet;
		for (size_t i = 0; i < (*v).size(); ++i)
		{
			std::vector<int> *tweetss = users[(*v)[i]-1].tweetVector();
			for (size_t j = 0; j < (*tweetss).size(); ++j)
			{
				alltweet.push_back((*tweetss)[j]);
			}
		}
		sort(alltweet.begin(),alltweet.end());
		for(int i=0;i<alltweet.size();i++)
		{
			cout<<tweets[alltweet[i]-1].getTweetUser()<<" "<<alltweet[i]<<" "<<tweets[alltweet[i]-1].getTweetText()<<endl;
		}		
		return;	

	}

	void creatingAreplyTweet(int &userId, int &tweetId, string &tweetText){
		if (tweetId > num_tweets || tweetId < 0)
		{
			cout<<"No such tweet exists\n";
		}
		else if (userId > num_users || userId < 0)
		{
			cout<<"UserID "<<userId<<" does not exist\n";
		}
		else {
			num_tweets++;
			Tweet newTweet(num_tweets,userId,tweetText,tweetId);
			tweets.push_back(newTweet);
			users[userId-1].addTweet(num_tweets);
			tweets[tweetId - 1].addreply(num_tweets);
			cout<<"UserID "<<userId<<" replied "<<tweetText<<" to tweet "<<tweets[tweetId-1].getTweetText()<<" and has TweetID "<<num_tweets<<"\n";
		}
		return;
	}

void printNestedTweet(int &tweetId, int recurseLevel){
	if(tweetId > num_tweets || tweetId < 0){
			cout<<"No such tweet exists\n";
	}
	else{
		for(int i = 0 ; i < recurseLevel; i++){
			cout<<"      ";
		}
		cout<<tweets[tweetId - 1].getTweetUser()<<" "<<tweetId<<" "<<tweets[tweetId - 1].getTweetText()<<"\n";
		std::vector<int> *v = tweets[tweetId - 1].replyVector();
		for (size_t i = 0; i < (*v).size(); ++i)
		{
			printNestedTweet((*v)[i],recurseLevel + 1);
		}
	}
	return;
}


};

int main()
{
	Network N;
	string qtype;
	while(true){
		cin>>qtype;
		if(qtype=="au")
		{
			string name;
			cin>>name;
			N.addUser(name);
		}
		else if(qtype=="pu")
		{
			N.printUsers();
		}
		else if(qtype=="fu")
		{
			int uid1,uid2;
			cin>>uid1>>uid2;
			if (uid1 == uid2)
			{
				cout<<"You cannot follow yourself\n";
			}
			else if(uid2>N.totalusers() || uid2<=0)
			{
				cout<<"UserID "<<uid2<<" does not exist\n";
			}
			else if(uid1>N.totalusers() || uid1<=0)
			{
				cout<<"UserID "<<uid1<<" does not exist\n";
			}
			else{
				User* usertoUpdate=N.getuser(uid1);
				(*usertoUpdate).addFollower(uid2);
			}
		}
		else if(qtype=="uu")
		{
			int uid1,uid2;
			cin>>uid1>>uid2;
			if (uid1 == uid2)
			{
				cout<<"You cannot follow yourself\n";
			}
			else if(uid2>N.totalusers() || uid2<=0)
			{
				cout<<"UserID "<<uid2<<" does not exist\n";
			}
			else if(uid1>N.totalusers() || uid1<=0)
			{
				cout<<"UserID "<<uid1<<" does not exist\n";
			}
			else{
				User* usertoUpdate = N.getuser(uid1);
				(*usertoUpdate).removeFollower(uid2);
			}
		}
		else if(qtype=="at")
		{
			int uid;
			string text;
			cin>>uid>>text;
			N.addTweet(uid,text);
		}
		else if(qtype=="pft")
		{
			int uid;
			cin>>uid;
			if(uid>N.totalusers() || uid<=0)
			{
				cout<<"UserID "<<uid<<" does not exist\n";
			}
			else {
				N.printFollowersTweet(uid);		}
			
		}
		else if(qtype=="rt")
		{
			int uid,tid;
			string text;
			cin>>uid>>tid>>text;
			N.creatingAreplyTweet(uid,tid,text);
		}
		else if(qtype=="nt")
		{
			int tid;
			cin>>tid;
			N.printNestedTweet(tid,0);
		}
		else if(qtype=="exit")
			break;
 }
}