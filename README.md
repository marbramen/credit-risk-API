# Deploy Docker

## Deploy all modules

```
$ cd {dir-project}
$ sudo docker build -t credit-risk .
$ sudo docker run -it -p 6924:6924 --name credit-risk --net=host credit-risk
```

These are examples of using the component

Example 01:

![picture](https://drive.google.com/uc?id=1HzB2jJgBr6SY5iGFt_fPMjErIC8vFHoS)

Example 02:

![picture](https://drive.google.com/uc?id=1s0xYWFaFfoMdrKQer8EdiOIgiGH73sJJ)

For more information read doc: 
```
MLE_Challenge_Implementation.pdf
```
