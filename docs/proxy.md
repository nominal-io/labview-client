# Connect through a proxy

{.lead}
On networks that reach the internet only through a proxy server, the client can send its traffic to
Nominal through that proxy.

## Turn on a proxy

The client connects directly unless you ask it to use a proxy. Set the **proxy server** input of
{lv:vi}`Create Nominal Client` to one of:

- A proxy address, such as `http://proxy.example.com:8080`, to always use that proxy.
- An empty string, to find the proxy as described below.
- `direct`, the default, to connect without a proxy.

Streams created with {lv:vi}`Create Stream (advanced)` take the same values on its own **proxy
server** input.

## How an empty value finds the proxy

With an empty **proxy server**, the client uses the first of these that is set:

1. **Environment variables.** Nominal is reached over HTTPS, so the client uses `HTTPS_PROXY`, or
   `ALL_PROXY` when that isn't set. Hosts listed in `NO_PROXY` connect directly.
2. **The Windows proxy setting**, under **Settings > Network & internet > Proxy > Manual proxy
   setup**. Addresses listed under **Use the proxy server except for addresses that start with the
   following entries** connect directly, and so do host names without a dot when **Don't use the
   proxy server for local (intranet) addresses** is checked. When `NO_PROXY` is set, it replaces
   this list. If the proxy is set per protocol (**Internet Options > Connections > LAN settings >
   Advanced**), the client uses the **Secure** entry.

With neither set, the client connects directly. A proxy address given in **proxy server** ignores
both bypass lists.

## Proxy addresses

- Write the proxy as `proxy.example.com:8080` or `http://proxy.example.com:8080`. Without a port,
  the client uses port 80.
- For a proxy that asks for a user name and password, include them:
  `http://user:password@proxy.example.com:8080`. Percent-encode special characters in either one,
  for example `%40` for `@` and `%3A` for `:`.
- The proxy itself must be an HTTP proxy. An `https://` or SOCKS proxy address is reported as an
  error rather than ignored.

In `NO_PROXY`, separate entries with commas. `example.com` or `.example.com` matches that domain and
its subdomains, and `*` matches every host. The Windows list separates entries with semicolons and
accepts `*` wildcards, such as `*.example.com`. IP ranges such as `10.0.0.0/8` aren't supported in
either list.

## When changes take effect

- A stream uses the proxy from when it was created.
- Requests use the **proxy server** of the most recently created client, for every client in the
  LabVIEW session. Create clients with the same setting if you use more than one.
- With an empty **proxy server**, the proxy is looked up again for each new client or stream, so a
  change to the Windows setting applies to clients and streams created after it. Environment
  variables set in Windows reach LabVIEW only when LabVIEW starts.

## Proxies that inspect HTTPS

Some company proxies decrypt and re-encrypt HTTPS traffic with their own certificate. The client
trusts the certificates in the Windows certificate store, so this works when the company's root
certificate is installed in Windows, as it usually is on managed machines.

## What isn't supported

- **Setup scripts and automatic detection.** The client ignores **Use setup script** (a PAC file)
  and **Automatically detect settings** (WPAD). If your network only offers these, ask your IT team
  for the proxy's address and port, and give it to **proxy server**.
- **Proxies that sign in with your Windows account** (NTLM or Kerberos). These proxies refuse the
  connection with HTTP 407, Proxy Authentication Required. Proxies that take a user name and
  password work.
- **SOCKS proxies.**

## NI Linux RT

NI Linux RT targets have no Windows proxy setting. There, an empty **proxy server** uses only the
environment variables.
