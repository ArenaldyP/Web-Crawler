import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
from fake_useragent import UserAgent

# Inisialisasi modul colorama untuk tampilan warna konsol
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# Inisialisasi himpunan link (Unique Links)
internal_urls = set()
external_urls = set()

# Membuat instance UserAgent untuk menghasilkan header User-Agent secara acak
user_agent = UserAgent()

def is_valid(url):
    """Fungsi untuk memeriksa apakah `url` adalah URL yang valid"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """Fungsi untuk mendapatkan semua URL yang ditemukan pada `url` yang merupakan bagian dari situs web yang sama"""
    # Semua URL pada `url`
    urls = set()
    # Nama domain URL tanpa protokol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url, headers={'User-Agent': user_agent.random}).content, "html.parser")  # Menggunakan User-Agent acak

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # Tag href kosong
            continue
        # Gabungkan URL jika bersifat relatif (bukan link absolut)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # Hapus parameter GET URL, fragmen URL, dll.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # Bukan URL yang valid
            continue
        if href in internal_urls:
            # Sudah ada dalam himpunan
            continue
        if domain_name not in href:
            # Link eksternal
            if href not in external_urls:
                print(f"{GRAY}[*] Link eksternal: {href} {RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Link Internal: {href} {RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

# Jumlah URL yang telah dikunjungi akan disimpan di sini
total_urls_visited = 0

def crawl(url, max_urls=30):
    """Fungsi untuk menjelajahi halaman web dan mengekstrak semua link.
    Anda akan menemukan semua link dalam variabel set global `external_urls` dan `internal_urls`.
    :params:
        max_urls(int): jumlah maksimal url yang ingin di-crawl, default adalah 30"""

    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Mengecrawl: {url} {RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

if __name__ == "__main__":
    website = input("Masukkan Website: ")
    max_urls = int(input("Masukkan jumlah maksimal URL yang ingin di-crawl: "))
    crawl(website, max_urls=max_urls)
    print(f"[+] Total Link Internal: {len(internal_urls)}")
    print(f"[+] Total Link Eksternal: {len(external_urls)}")
    print(f"[+] Total URL: {len(external_urls) + len(internal_urls)}")
    print(f"[+] Total URL yang Dikunjungi : {total_urls_visited}")
