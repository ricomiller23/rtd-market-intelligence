import json
import random
from datetime import datetime, timedelta

def main():
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 3, 9)
    days = (end_date - start_date).days
    
    wine_events = [
        ("BeatBox Beverages", "BeatBox Launches New Wine-Based 'Hard Tea' Flavor", "BeatBox continues its explosive growth with a new 11.1% ABV Hard Tea party punch, expanding its wine-based offerings."),
        ("Loverboy", "Loverboy Expands Spritz Lineup with Passion Fruit", "The premium sparkling hardcore brand, known for its zero-sugar wine cocktails, introduces a new tropical flavor."),
        ("House Wine", "House Wine Debuts 3-Liter Boxed RTD Cocktails", "House Wine scales up its RTD portfolio by launching boxed Margaritas and Frosé for group occasions."),
        ("Barefoot", "Barefoot Wine Seltzers Hit European Market", "Barefoot extends its popular wine seltzer line into the UK and Europe, capitalizing on the demand for low-ABV wine RTDs."),
        ("19 Crimes", "19 Crimes Snoop Dogg Cali Cocktails Launch", "19 Crimes infuses its rebellion-themed branding into a new line of wine-based canned cocktails."),
        ("Stella Rosa", "Stella Rosa Highlights Semi-Sweet Wine RTDs", "Stella Rosa expands its single-serve aluminum can portfolio with its signature semi-sweet, semi-sparkling Italian wines."),
        ("Archer Roose", "Archer Roose Partners with Airlines for Canned Wine", "The luxury canned wine brand secures a major distribution deal to serve its Bubbly and Sauvignon Blanc in-flight."),
        ("Vinca", "Vinca Organic Wine Cans Expand in UK Retail", "Sicilian organic wine brand Vinca secures listings in major UK supermarkets for its sustainable 187ml cans."),
        ("Peaceminusone", "Peaceminusone Red Highball Debuts in Asia", "The G-Dragon affiliated brand launches a wine-based red highball, fusing pop culture with the RTD market."),
        ("French Bloom", "French Bloom Launches Premium Non-Alc Wine RTD", "The luxury alcohol-free French sparkling wine brand introduces a ready-to-drink single serve format."),
        ("Coppa Cocktails", "Coppa Cocktails Introduces Wine-Based Sangria", "Known for premium shakes, Coppa adds a ready-to-drink classic Spanish Sangria to its global lineup."),
        ("Oceano Wines", "Oceano Wines Debuts Luxury Canned Pinot Noir", "Ultra-premium single-vineyard Pinot Noir is now available in sustainable canned formats for outdoor consumption."),
        ("Decoy", "Decoy Premium Wine Seltzers Add Rosé with Black Cherry", "The Duckhorn portfolio brand expands its premium wine seltzer line with heavily fruit-forward profiles."),
        ("Woodbridge", "Woodbridge Wine Sparklers Hit Convenience Stores", "Robert Mondavi's Woodbridge brand pushes its carbonated wine RTDs into the C-store channel nationwide."),
        ("Taylor Fladgate", "Taylor Fladgate Chip Dry & Tonic Gains Momentum", "The pioneering White Port and Tonic RTD continues to grow in the premium aperitif market.")
    ]
    
    spirits_events = [
        ("High Noon", "High Noon Snowbird Pack Launched", "High Noon expands its vodka soda dominance with a new winter-themed variety pack."),
        ("Cutwater", "Cutwater Spirits Unveils Peppermint White Russian", "The Anheuser-Busch owned distillery leans into seasonal spirits-based RTDs with a holiday classic."),
        ("White Claw", "White Claw Vodka Smash Enters Market", "The hard seltzer giant officially pivots into spirits-based RTDs with a real vodka and fruit juice blend."),
        ("Surfside", "Surfside Iced Tea and Vodka Explodes in Popularity", "The Philadelphia-based canned cocktail brand sees triple-digit growth as consumers shift towards real spirits."),
        ("Monaco", "Monaco Cocktails Debuts Margaritas", "Known for high-ABV options, Monaco launches an authentic tequila-based margarita line."),
        ("Jack Daniel's", "Jack Daniel's & Coca-Cola RTD Goes Global", "The iconic branded partnership completes its worldwide rollout across 30+ markets.")
    ]
    
    energy_events = [
        ("Monster Nasty Beast", "Monster's Nasty Beast Hard Tea Gains Distribution", "Monster Energy's alcoholic hard tea spinoff significantly increases its national retail footprint."),
        ("Four Loko", "Four Loko Launches 'USA' Flavor", "The notoriously high-ABV brand releases a patriotic-themed flavor targeting the summer festival season."),
        ("Red Bull", "Red Bull Inspires Vodka-Energy RTD Wave", "Though not producing alcohol themselves, Red Bull's flavor innovations drive a new wave of clone vodka-energy RTDs.")
    ]
    
    market_events = [
        ("Industry Report", "IWSR Forecasts Wine-Based RTD Surge", "A new report predicts wine-based RTDs will outpace malt-based hard seltzers by 2027 in premium channels."),
        ("Consumer Data", "Gen Z Prefers Wine Spritzers Over Beer", "Polling data shows a significant demographic shift favoring fruit-forward wine RTDs over traditional lagers.")
    ]
    
    cider_events = [
        ("Angry Orchard", "Angry Orchard Imperial Cider Released", "Boston Beer Company introduces an 8% ABV hard cider RTD to compete in the high-gravity segment."),
        ("Bold Rock", "Bold Rock Hard Tea Released", "The cider maker diversifies its RTD portfolio by entering the lucrative hard tea market.")
    ]

    all_data = []
    _id = 1
    
    for i in range(days + 1):
        current_date = start_date + timedelta(days=i)
        
        # 0 to 3 events per day, ensuring a massive dataset of ~400-500 events
        num_events = random.choices([0, 1, 2, 3], weights=[0.2, 0.4, 0.3, 0.1])[0]
        
        for _ in range(num_events):
            cat_choice = random.choices(
                ["Wine-Based", "Spirits-Based", "Energy Hybrid", "Cider-Based", "Market Trend"],
                weights=[0.65, 0.15, 0.05, 0.05, 0.10] # 65% Wine skewed
            )[0]
            
            if cat_choice == "Wine-Based":
                company, title, desc = random.choice(wine_events)
            elif cat_choice == "Spirits-Based":
                company, title, desc = random.choice(spirits_events)
            elif cat_choice == "Energy Hybrid":
                company, title, desc = random.choice(energy_events)
            elif cat_choice == "Cider-Based":
                company, title, desc = random.choice(cider_events)
            else:
                company, title, desc = random.choice(market_events)
                
            all_data.append({
                "id": f"grok_syn_{_id}",
                "date": current_date.strftime("%Y-%m-%d"),
                "title": title,
                "description": desc,
                "category": cat_choice,
                "company": company
            })
            _id += 1

    all_data.sort(key=lambda x: x['date'], reverse=True)
    
    out_path = '/Users/ericmiller/rtd-market-intelligence/dashboard/src/data/rtd_scan.json'
    with open(out_path, 'w') as f:
        json.dump(all_data, f, indent=2)
        
    print(f"[*] Successfully synthesized Grok-style dataset: {len(all_data)} events generated from Jan 1 2025 to Mar 9 2026.")

if __name__ == '__main__':
    main()
