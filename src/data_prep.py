import urllib.request
import os


URL_SOLUTIONS = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt"
URL_ALLOWED = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
def build_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print(f"Fetching word list...")
    try:
        with urllib.request.urlopen(URL_SOLUTIONS) as response:
            raw_data = response.read().decode('utf-8')
            all_words = raw_data.splitlines()
            
        print(f"Total solution words fetched: {len(all_words)}")
        print(f"Sample words: {all_words[:5]}")

        for length in [5, 6, 7]:
            # Clean and filter
            filtered = [w.strip().lower() for w in all_words if len(w.strip()) == length]
            
            if not filtered:
                print(f"⚠️ Warning: No {length}-letter words found!")
                continue

            filename = os.path.join(data_dir, f"solutions_{length}.txt")
            with open(filename, "w") as f:
                f.write("\n".join(filtered))
            print(f"✅ Success! Created {filename} ({len(filtered)} words).")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    try:
        with urllib.request.urlopen(URL_ALLOWED) as response:
            words = response.read().decode('utf-8').splitlines()
        print(f"Total allowed words fetched: {len(words)}")
        print(f"Sample words: {words[:5]}")
        
        cleaned = [w.strip().lower() for w in words]
        filename = os.path.join(data_dir, "allowed.txt")
        with open(filename, "w") as f:
            f.write("\n".join(cleaned))
        print(f"✅ Success! Created {filename} ({len(cleaned)} words)")
    except Exception as e:
        print(f"❌ Error: {e}")
        
        
            

if __name__ == "__main__":
    build_data()