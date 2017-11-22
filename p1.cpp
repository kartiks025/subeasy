#include <bits/stdc++.h>
using namespace std;

void merge(int arr[], int l, int m, int r){
	
	int n1 =m- l +1;
	int n2 = r-m+1 ;
	int L[n1];
	int R[n2];
	//int arr[n+m];
	for(int i = 0;i<n1;i++){
		L[i] = arr[i+l];
	}

	for(int i = 0;i<n2;i++){
		R[i] = arr[m+1+i];
	}

	int i = 0,j = 0,k = l;

	while(i<n1 && j<n2){
		if(L[i] < R[j]){
			arr[k] = L[i];
			i++;
			k++;
		}

		else{
			arr[k] = R[j];
			j++;
			k++;
		}
	}

	while(i<n1){
		arr[k] = L[i];
		k++;
	}

	while(j<n2){
		arr[k] = R[j];
		k++;
	}



	
}

void mergesort(int a[], int n, int start, int end){
	int mid = start+ (end-1)/2;
	while(start<=end){
		start = mid;
		mergesort(a,end-start,start, end);
		merge(a,start,mid,end);
	} 

}

void print_array(int a[], int n){
	sort(a, a+n);
	for(int i = 0;i<n;i++){
		cout<<a[i]<<" ";
	}
	cout<<endl;
}


int main(){
	int aa=1e7;
	int A[aa];
	for(int i=0;i<aa;i++)A[i]=0;
	int n,m;
	cin>>n;
	int a[n]; //int b[m];
	for(int i = 0;i<n;i++){
		cin>>a[i];
	}
	/*for(int i = 0;i<m;i++){
		cin>>b[i];
	}*/
	print_array(a,n);
}





