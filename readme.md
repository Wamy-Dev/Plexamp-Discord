# Plexamp Discord RPC

![full_preview](/previews/full_preview.png)

## Setup

1. First, you will need to proxy your Plex server. For this, I am using Cloudflare tunnels (only for API routes, explained below), as this provides easy setup with little to no configuration. Read below on how to setup Cloudflare Tunnels for this purpose. This is necessary for images, as they need to be publicly accessible.
2. Once your Plex server is proxied, enter your details into `config.example.json`. This includes your new proxied Plex server URL as "public_plex_url".
3. Copy this config to `config.json` wherever your service is running on your device.
4. Run the service, and press play on Plexamp!

## Cloudflare Tunnels

While streaming video through Cloudflare tunnels isn't allowed, using the Plex internal API to be exposed publicly is. Go to https://one.dash.cloudflare.com and login to your Cloudflare account or create a new account. Go to Networks -> Tunnels and click the button labeled, "Create a tunnel". Follow the instructions to install to your machine. When asked to publish an application route, make sure your domain is on your Cloudflare account and create a URL. While you don't have to use Cloudflare tunnels, using something like Nginx, will have all of these same configuration options available.

For subdomain, I used `plex` but you can put anything.

For domain, pick your domain.

For path, use `library/metadata`. This is necessary to prevent people from publicly accessing your Plex server, since this is necessary for Discord to see it, as well as the service exposing your X-Plex-Token. __DO NOT MISS THIS STEP__.

For service, choose type, `HTTPS`, and point URL to your internal IP of your Plex server. Mine is `127.0.0.1:32400`.

Under "Additional application settings" go to TLS and enable `No TLS Verify`. This is necessary as Plex runs on HTTPS, but doesn't have a signed certificate (unless you explicitly added one).

## Running

There are 2 ways of running this service. One way is locally on your device, it will start and stop whenever you boot up your computer. The other way is running this in a Docker compose using [kasmweb/discord](https://hub.docker.com/r/kasmweb/discord) Docker container, to connect the 2 together.


## Compatbility

This application is only compatible with Unix devices. Windows has a different socket communication process that is not built into this service. If running on Windows, use the Docker method of installation and running.

## Previews

![preview_1](/previews/preview_1.png)
![preview_2](/previews/preview_2.png)
![preview_3](/previews/preview_3.png)

