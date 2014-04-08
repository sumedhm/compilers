#include <stdio.h>
#include <stdlib.h>
int main()
{
	int T, t;
	scanf("%d", &T);
	for (t = 0; t < T; t++)
	{
		int *stock, max = 0, min, n, k = 2, i, j, x;
		scanf("%d", &n);
		int maxprofit[n+1][2];
		stock = (int *) malloc (sizeof(int)*(n+1));
		stock[0] = 0;
		for(i=1; i<n+1; i++){
			scanf("%d", &stock[i]);
			if(stock[i]>max)
				max = stock[i];
		}
		for (i=0; i<n+1; i++)
		{
			maxprofit[i][0] = 0;
			maxprofit[i][1] = 0;
		}
		for(i=1; i<k+1; i++){
			min = max + 1;
			for(j=2; j<n+1; j++){
				if((stock[j-1] - maxprofit[j-2][0]) < min)
					min = stock[j-1] - maxprofit[j-2][0];
				x = stock[j] - min;
				if((x > maxprofit[j][1]) && (x >= maxprofit[j-1][1]))
					maxprofit[j][1] = x;
				if((maxprofit[j-1][1] > maxprofit[j][1]) && (maxprofit[j-1][1] > x))
					maxprofit[j][1] = maxprofit[j-1][1];
			}
			for(j=0; j<n+1; j++)
				maxprofit[j][0] = maxprofit[j][1];
		}
		printf("%d\n", maxprofit[n][1]);

	}
	return 0;
}
