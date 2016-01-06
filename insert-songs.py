import time
import struct
import urllib.parse, urllib.request


def construct_request_body(timestamp, itunes_identifier):
    hex = "61 6a 43 41 00 00 00 45 6d 73 74 63 00 00 00 04 55 94 17 a3 6d 6c 69 64 00 00 00 04 00 00 00 00 6d 75 73 72 00 00 00 04 00 00 00 81 6d 69 6b 64 00 00 00 01 02 6d 69 64 61 00 00 00 10 61 65 41 69 00 00 00 08 00 00 00 00 11 8c d9 2c 00"

    body = bytearray.fromhex(hex);
    body[16:20] = struct.pack('>I', timestamp)
    body[-5:] = struct.pack('>I', itunes_identifier)
    return body


def add_song(itunes_identifier):
    data = construct_request_body(int(time.time()), itunes_identifier)

    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0",
        "Client-iTunes-Sharing-Version" : "3.12",
        "Accept-Language" : "nl-nl, nl;q=0.83, fr-fr;q=0.67, fr;q=0.50, en-us;q=0.33, en;q=0.17",
        "Client-Cloud-DAAP-Version" : "1.0/iTunes-12.2.0.145",
        "Accept-Encoding" : "gzip",
        "X-Apple-itre" : "0",
        "Client-DAAP-Version" : "3.13",
        "User-Agent" : "iTunes/12.3.2 (Macintosh; OS X 10.11.2) AppleWebKit/601.3.9",
        "Connection" : "keep-alive",
        "Content-Type" : "application/x-dmap-tagged",
        # Replace the values of the next three headers with the values you intercepted
        "X-Dsid" : "94537765",
        "Cookie" : "amia-94537765=3NlgaslZ/NkMghat4htbbml5mVwcughHw1RaIcPvmYLJuzq070TN0NT/zBANlt49/cFnMP3s9kB0xvp0ovnqtQ==; amp=zemDjHTK6zugtKsZJyegKfYsoV7r5wDbVNzOxU3S/RHSUfB54C/FK/UvBU4DGiagHQl2JBZYlAVuw4BZWPWFOdAa8t2YscpnpK7GAzHswOWMs2LGhYrczIJdM4K3GBoUImKwetP+PThcKvjmGkfD3zbokbjbNoDTtBS29jhm/2JoTQlBswPqjniw7fy7OYItLZ0OKA4xGH2bXsgCd90kEwdOfTQLaMvORSB4wNiEbxLFN/JESEtDnuqraoQQayFJ; mt-asn-94537765=15; mt-tkn-94537765=ApvTi/XpXgSMSy6dFJqehoXtzXAjk7QAMNTl2GUpZL/Nxj+p9y7nj0oOBxG2KS0wtzQYqeBGBm536wh0R674aJ1IW/T0jv1qQuYaAidwH8VEpv/SV7qKToiSWK7C4Kgz2wuBQDu+Gl3hmIOBFju+4/MrBed95FY/8Gsa1qidwblGKIJ8wOclecuFnWaAgjxk6Y/34Gw=; mzf_in=502440; TrPod=4; X-Dsid=94537765; itspod=50; mz_at0-94537765=AwQAAAEBAAHV7gAAAABWedbOzrHm9kgoLE+sw2K/+u3lw8tONx0=; mz_at_ssl-94537765=AwUAAAEBAAHV7gAAAABWedbO8xZty5r5JTAZH1Gqb8XgZ10DDXY=; ns-mzf-inst=179-44-443-215-23-8160-502440-50-st13; s_vi=[CS]v1|2B3CEF8585012FB8-600001370006D297[CE]; xp_ci=3z2HjWUdz3UXz5ErzB19zXkakdO0d",
        "X-Guid" : "A8206622DC71",
        "Content-Length" : "77"
    }

    request = urllib.request.Request("https://ld-4.itunes.apple.com/WebObjects/MZDaap.woa/daap/databases/1/cloud-add", data, headers)
    urllib.request.urlopen(request)


with open('itunes.csv') as itunes_identifiers_file:
    for line in itunes_identifiers_file:
        itunes_identifier = int(line)

        try:
            add_song(itunes_identifier)
            print("Successfuly inserted a song!")
            # Try playing with the interval here to circumvent the API rate limit
            time.sleep(10)
        except Exception as e:
            print("Something went wrong while inserting " + str(itunes_identifier) + " : " + str(e))