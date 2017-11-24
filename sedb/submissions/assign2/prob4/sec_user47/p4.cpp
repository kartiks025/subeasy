#include <iostream>
#include <vector>

using namespace std;
vector<long long int> v(300005);

long long int merge(long long int l,long long int m,long long int r){
	long long int sx=m-l;
	long long int sy=r-m;
	long long int a[sx],b[sy];
	for(long long int i=0;i<sx;i++) a[i]=v[i+l];
	for(long long int i=0;i<sy;i++) b[i]=v[m+i];
	long long int ans=0;
	long long int p=0;
	for(long long int i=0;i<sy;i++){
		while(p<sx && a[p]<= b[i]) p++;
		ans+=(sx-p);
	}
	long long int i=0,j=0,k=l;
	while(i < sx && j < sy){
		if(a[i]>b[j]){
			v[k]=b[j];
			j++;
		}
		else{
			v[k]=a[i];
			i++;
		}
		k++;
	}
	while(i<sx){
		v[k]=a[i];
		k++;
		i++;
	}
	while(j<sy){
		v[k]=b[j];
		k++;
		j++;
	}
	return ans;	
}

long long int merge_sort(long long int l,long long int r){
	if(l>=r) return 0;
	if(r==l+1) return 0;
	long long int m=(l+r)/2;
	long long int x=merge_sort(l,m);
	
	long long int y=merge_sort(m,r);

	long long int z=merge(l,m,r);
	return x+y+z;
}

int main(){
	long long int n;
	cin>>n;
	for(long long int i=0;i<n;i++) cin>>v[i];
	cout<<merge_sort(0,n)<<endl;

}