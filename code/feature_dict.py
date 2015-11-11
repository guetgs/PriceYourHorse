import numpy as np

Sex_dict = {u'Broodmare': 'Broodmare', u'Colt': 'Colt/Filly',\
            u'Filly': 'Colt/Filly', u'Foal': 'Foal/Yearling',\
            u'Gelding': 'Adult', u'Mare': 'Adult', u'Ridgling': 'Ridgling',\
            u'Stallion': 'Adult', u'Unborn Foal': 'Unborn Foal',\
            u'Weanling': 'Foal/Yearling', u'Yearling': 'Foal/Yearling',\
            u'Unknown': 'Foal/Yearling', u'-': None, np.nan: None}


Color_dict = {u'Bay': 'Other', u'Bay Overo': 'Other', u'Bay Roan': 'Other',\
              u'Black': 'Other', u'Black Overo': 'Other',\
              u'Blue Grulla': 'Other', u'Blue Roan': 'Other',\
              u'Brindle': 'Brindle', u'Brown': 'Other',\
              u'Buckskin': 'Other', u'Buckskin Overo': 'Other',\
              u'Champagne': 'Other', u'Chestnut': 'Other',\
              u'Chestnut Overo': 'Other', u'Chocolate': 'Other',\
              u'Cremello': 'Other', u'Dun': 'Other', \
              u'Dun w/ Blk Points': 'Other', u'Dunalino': 'Other',\
              u'Dunskin': 'Other', u'Grey': 'Grey', u'Grulla': 'Other',\
              u'Liver Chestnut': 'Other', u'Other': 'Other',\
              u'Overo': 'Other', u'Palomino': 'Other',\
              u'Perlino': 'Other', u'Piebald': 'Piebald',\
              u'Pinto': 'Other', u'Red Dun': 'Other', u'Red Roan': 'Other',\
              u'Roan': 'Other', u'Sabino': 'Other', u'Smokey Black': 'Other',\
              u'Sorrel': 'Other', u'Sorrel Overo': 'Other',\
              u'Tobiano': 'Other', u'Tovero': 'Other', u'Unknown': 'Other',\
              u'White': 'Other', u'sil': 'Other', u'-': 'Other', np.nan: 'Other'}

Breeds_dict = {u'Akhal Teke': 'Akhal Teke',
               u'American Cream': 'Other',
               u'Andalusian': 'Andalusian',
               u'Appaloosa': 'Appaloosa',
               u'Appendix': 'Other',
               u'AraAppaloosa': 'AraAppaloosa',
               u'Arabian': 'Arabian',
               u'Araloosa': 'AraAppaloosa',
               u'Australian Stock': 'Other',
               u'Azteca': 'Azteca',
               u'Barb': 'Barb',
               u'Bashkir Curly': 'Bashkir Curly',
               u'Belgian': 'Belgian',
               u'Belgian Warmblood': 'Belgian Warmblood',
               u'Canadian': 'Canadian',
               u'Chincoteague Pony': 'Chincoteague Pony',
               u'Cleveland Bay': 'Cleveland Bay',
               u'Clydesdale': 'Clydesdale',
               u'Connemara Pony': 'Connemara Pony',
               u'Crossbred Pony': 'Crossbred Pony',
               u'Curly': 'Curly',
               u'Dales Pony': 'Dales Pony',
               u'Dartmoor Pony': 'Pony',
               u'Donkey': 'Donkey',
               u'Draft': 'Draft',
               u'Drum': 'Drum',
               u'Dutch Warmblood': 'Dutch Warmblood',
               u'Exmoor Pony': 'Exmoor Pony',
               u'Fell Pony': 'Fell Pony',
               u'Fjord': 'Fjord',
               u'Florida Cracker': 'Florida Cracker',
               u'Friesian': 'Friesian',
               u'Gotland Pony': 'Pony',
               u'Gypsy Vanner': 'Gypsy Vanner',
               u'Hackney': 'Hackney',
               u'Haflinger': 'Haflinger',
               u'Half Arabian': 'Half Arabian',
               u'Hanoverian': 'Hanoverian',
               u'Highland Pony': 'Pony',
               u'Holsteiner': 'Holsteiner',
               u'Hungarian': 'Hungarian',
               u'Iberian': 'Iberian',
               u'Icelandic': 'Icelandic',
               u'Irish Draught': 'Irish Draught',
               u'Kentucky Mountain': 'Other',
               u'Knabstrupper': 'Knabstrupper',
               u'Lipizzan': 'Lipizzan',
               u'Lusitano': 'Lusitano',
               u'Marchador': 'Other',
               u'Miniature': 'Miniature',
               u'Missouri Fox Trotter': 'Missouri Fox Trotter',
               u'Morab': 'Morab',
               u'Morgan': 'Morgan',
               u'Mountain Pleasure': 'Other',
               u'Mule': 'Mule',
               u'Mustang': 'Mustang',
               u'National Show': 'Other',
               u'Natl Sport Perf. Pony': 'Pony',
               u'New Forest Pony': 'New Forest Pony',
               u'Newfoundland Pony': 'Newfoundland Pony',
               u'Nokota': 'Nokota',
               u'Oldenburg': 'Oldenburg',
               u'Other': 'Other',
               u'POA': 'Other',
               u'Paint': 'Paint',
               u'Paint Pony': 'Paint Pony',
               u'Palomino': 'Palomino',
               u'Paso Fino': 'Paso Fino',
               u'Percheron': 'Other',
               u'Peruvian Paso': 'Paso Fino',
               u'Pintabian': 'Half Arabian',
               u'Pinto': 'Pinto',
               u'Pony': 'Pony',
               u'Quarab': 'Other',
               u'Quarter Horse': 'Quarter Horse',
               u'Quarter Pony': 'Quarter Pony',
               u'Racking': 'Other',
               u'Rocky Mountain': 'Other',
               u'Saddlebred': 'Saddlebred',
               u'Selle Francais': 'Selle Francais',
               u'Shetland Pony': 'Shetland Pony',
               u'Shire': 'Shire',
               u'Single Footing': 'Other',
               u'Spanish Mustang': 'Mustang',
               u'Spotted': 'Spotted',
               u'Spotted Saddle': 'Saddlebred',
               u'Standardbred': 'Standardbred',
               u'Tennessee Walking': 'Tennessee Walking',
               u'Thoroughbred': 'Thoroughbred',
               u'Tiger': 'Other',
               u'Trakehner': 'Trakehner',
               u'Unknown': 'Other',
               u'Walkaloosa': 'Walkaloosa',
               u'Warmblood': 'Warmblood',
               u'Welsh Cob': 'Welsh Cob',
               u'Welsh Pony': 'Welsh Pony',
               u'Westphalian': 'Westphalian',
               u'-': None, np.nan: None} 