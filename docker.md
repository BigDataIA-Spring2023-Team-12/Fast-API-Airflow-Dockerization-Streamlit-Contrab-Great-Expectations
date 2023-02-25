Step 1:\
```docker build -t my-streamlit-app -f Dockerfile.streamlit .```


Step 2:\
```docker run -p 8501:8501 my-streamlit-app```