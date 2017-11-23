#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;


class User{

public:
	int userID;			// unique user id 
	string username;	// username. 
	vector<int> mytweets;	// vector of tweet ids which the user has posted.
	vector<int> following;	// vector of user ids followed by the user. 

	static int usercount;
	User(string uname){
		username = uname;
		userID = ++usercount;
	}
	void Follow(int id){
		following.push_back(id);
	}
	bool isFollowing(int id2){
		for(size_t i=0;i<following.size();i++){
			if(following[i]==id2)
				return true;
		}
		return false;
	}

	void Unfollow(int id2){
		for(size_t i=0;i<following.size();i++){
			if(following[i]==id2){
				following.erase(following.begin()+i);
				return;
			}
		}
	}

	void printFollowing(){
		sort(following.begin(),following.end());
		for(size_t i=0;i<following.size();i++){
			cout<<following[i]<<" ";
		}	
		cout<<endl;
	}

	void AddTweet(int id){
		mytweets.push_back(id);
	}
};

int User::usercount = 0;

class Tweet{
public:
	int tweetID;		// unique tweet id,
	int parentTweetID;	// parent tweet id - the tweet id of the tweet it is a reply of, if there is no parent store -1 as value.
	int tweeter;		// user id (denoting which user tweeted this) 
	vector<int> replies;	// vector of reply tweets id - contains the ids of tweets which are reply to this tweet.
	string tweetText;	// Tweet-text.
	static int tweetcount;

	Tweet(int uid,string tText){
		tweetID = ++tweetcount;
		tweeter = uid;
		tweetText = tText;
		parentTweetID = -1;
	}

	Tweet(int parentTID,int uid,string tText){
		tweetID = ++tweetcount;
		tweeter = uid;
		tweetText = tText;
		parentTweetID = parentTID;
	}

	void print(){
		cout<<tweetID<<" "<<tweetText<<endl;
	}

	void printWithUser(){
		cout<<tweeter<<" "<<tweetID<<" "<<tweetText<<endl;
	}

};

int Tweet::tweetcount = 0;

class Network{
	vector<User> users;		//vector containing all users in the network
	vector<Tweet> tweets;	//vector containing all tweets 
public:
	void AddUser();
	void GetUser();
	void PrintUsers();
	void FollowUser();
	void UnfollowUser();
	void PrintFollowedUsers();
	void AddTweet();
	void GetTweet();
	void PrintTweets();
	void PrintFollowingTweets();
	void ReplyTweet();
	void PrintNested(int ,int);
	void PrintTweetWithReplies();
	
};

//30 min class structure


// 4min
void Network::AddUser(){
	string uname;
	cin>>uname;
	users.push_back(User(uname));
	cout<<"User "<<uname<<" added. User ID: "<<users[users.size()-1].userID<<endl;
}


//2 min
void Network::PrintUsers(){
	for(int i=0;i<users.size();i++){
		cout<<users[i].userID<<" "<<users[i].username<<endl;
	}
}

//7 min
void Network::FollowUser(){
	int id1,id2;
	cin>>id1>>id2;
	if(id2<1 || id2> users.size()){
		cout<<"UserID "<<id2<<" does not exist"<<endl;
		return;
	}
	if(id1<1 || id1> users.size()){
		cout<<"UserID "<<id1<<" does not exist"<<endl;
		return;
	}
	if(id1==id2){
		cout<<"You cannot follow yourself"<<endl;
		return;
	}

	if(users[id1-1].isFollowing(id2)){
		cout<<"UserID "<<id1<<" is already following UserID "<<id2<<endl;
		return;
	}

	users[id1-1].Follow(id2);
	cout<<"UserID "<<id1<<" has started following UserID "<<id2<<endl;


}

//7 min
void Network::UnfollowUser(){

	int id1,id2;
	cin>>id1>>id2;
	if(id2<1 || id2> users.size()){
		cout<<"UserID "<<id2<<" does not exist"<<endl;
		return;
	}
	if(id1<1 || id1> users.size()){
		cout<<"UserID "<<id1<<" does not exist"<<endl;
		return;
	}

	if(users[id1-1].isFollowing(id2)){
		users[id1-1].Unfollow(id2);
		cout<<"UserID "<<id1<<" has unfollowed UserID "<<id2<<endl;
		return;
	}

	cout<<"UserID "<<id1<<" is not following UserID "<<id2<<endl;

}

//10 min
void Network::AddTweet(){
	int id;
	string tweet;
	cin>>id>>tweet;

	if(id<1 || id> users.size()){
		cout<<"UserID "<<id<<" does not exist"<<endl;
		return;
	}
	tweets.push_back(Tweet(id,tweet));
	users[id-1].AddTweet(tweets[tweets.size()-1].tweetID);	
	cout<<"UserID "<<id<<" tweeted "<<tweets[tweets.size()-1].tweetText<<endl;
}

//8 min
void Network::PrintFollowingTweets(){
	int id;
	cin>>id;
	if(id<1 || id> users.size()){
		cout<<"UserID "<<id<<" does not exist"<<endl;	
		return;
	}
	vector<int> following = users[id-1].following;
	vector<int> tweetID;
	for(int i=0;i<following.size();i++){
		tweetID.insert(tweetID.end(), users[following[i]-1].mytweets.begin(), users[following[i]-1].mytweets.end());
	}
	sort(tweetID.begin(),tweetID.end());
	for(int i=0;i<tweetID.size();i++){
		tweets[tweetID[i]-1].printWithUser();
	}
}

//10 min
void Network::ReplyTweet(){
	int id,parentTweetID;
	string tweet;
	cin>>id>>parentTweetID>>tweet;


	if(parentTweetID<1|| parentTweetID> tweets.size()){
		cout<<"No such tweet exists"<<endl;
		return;
	}
	if(id<1 || id> users.size()){
		cout<<"UserID "<<id<<" does not exist"<<endl;
		return;
	}

	
	tweets.push_back(Tweet(parentTweetID, id,tweet));
	users[id-1].AddTweet(tweets[tweets.size()-1].tweetID);	
	tweets[parentTweetID-1].replies.push_back(tweets[tweets.size()-1].tweetID);	
	cout<<"UserID "<<id<<" replied "<<tweets[tweets.size()-1].tweetText <<" to tweet "<<tweets[parentTweetID-1].tweetText<<" and has TweetID "<<tweets[tweets.size()-1].tweetID<<endl;

}

void Network::PrintNested(int id,int offset=0){
	for(int i=0;i<offset;i++)
		cout<<" ";
	tweets[id-1].printWithUser();
	for(int i=0;i<tweets[id-1].replies.size();i++){
		PrintNested(tweets[id-1].replies[i],offset+6);
	}
}

//12 min
void Network::PrintTweetWithReplies(){
	int tid;
	cin>>tid;

	if(tid<1|| tid> tweets.size()){
		cout<<"No such tweet exists"<<endl;
		return;
	}

	PrintNested(tid);
}








// 10 min for main
int main(){
	Network twitter;
	while(true){
		string q;
		cin >> q;
		if(q== "au")	
			twitter.AddUser();
			
		else if(q== "pu")	
			twitter.PrintUsers();
			
		else if(q== "fu")	
			twitter.FollowUser();
			
		else if(q== "uu")	
			twitter.UnfollowUser();
		
		else if(q== "at")	
			twitter.AddTweet();
		
		else if(q=="rt")
			twitter.ReplyTweet();

		else if(q== "pft")
			twitter.PrintFollowingTweets();
		
		else if(q== "nt")	
			twitter.PrintTweetWithReplies();

		else if(q=="exit")
			break;
				
	}
}