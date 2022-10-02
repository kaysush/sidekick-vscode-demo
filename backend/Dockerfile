FROM node:16.13.1-stretch as build

WORKDIR /app

COPY package*.json /app/

# Install production dependencies
RUN npm install --only=production
RUN cp -a node_modules /tmp/prod_node_modules

# Now install all dependencies
RUN npm install

COPY . .

FROM gcr.io/distroless/nodejs:16
COPY --from=build --chown=nonroot:nonroot /tmp/prod_node_modules/ /app/node_modules/
WORKDIR /app
COPY . .
USER nonroot
CMD ["index.js"]
