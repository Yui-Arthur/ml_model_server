FROM node
WORKDIR /usr/src/app
COPY ./API_server/package*.json ./
RUN npm install
COPY ["API_server" , "./"]
CMD ["node" , "app.js" ]
