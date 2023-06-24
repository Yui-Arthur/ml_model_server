FROM python
WORKDIR llm_server
COPY ["./model_*.py" , "./prepare.sh" , "./"] 
RUN chmod 777 ./prepare.sh && bash ./prepare.sh
CMD ["python" , "model_server.py" ]
