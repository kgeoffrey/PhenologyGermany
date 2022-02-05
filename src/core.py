import pandas as pd


class PhenologicalData:
    
    def __init__(self):
        self.save_path = './data/raw/'
        self.root_path = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/annual_reporters'
        self.plant_paths = {
            'apfel_frueh' : '/fruit/historical/PH_Jahresmelder_Obst_Apfel_fruehe_Reife_1929_2020_hist.txt',
            'forsynthie' : '/wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Forsythie_1945_2020_hist.txt',
            'hasel' : '/wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Hasel_1930_2020_hist.txt',
            'holunder' : '/wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Schwarzer_Holunder_1925_2020_hist.txt',
            'stiel_eiche' : '/wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Stiel-Eiche_1925_2020_hist.txt',
            'sommer_linde' : '/wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Sommer-Linde_1925_2020_hist.txt',
        }
        self.seasons = {
            'Vorfrühling' : {'Phasen_ID': 5, 'plant_name': 'hasel'},
            'Erstfrühling': {'Phasen_ID': 5, 'plant_name': 'forsynthie'},
            'Vollfrühling': {'Phasen_ID': 5, 'plant_name': 'apfel_frueh'},
            'Frühsommer': {'Phasen_ID': 5, 'plant_name': 'holunder'}, 
            'Hochsommer': {'Phasen_ID': 5, 'plant_name': 'sommer_linde'},
            'Spätsommer': {'Phasen_ID': 29, 'plant_name': 'apfel_frueh'},
            'Früherbst': {'Phasen_ID': 62, 'plant_name': 'holunder'},
            'Vollherbst': {'Phasen_ID': 62, 'plant_name': 'stiel_eiche'},
            'Spätherbst': {'Phasen_ID': 31, 'plant_name': 'stiel_eiche'},
            'Winter': {'Phasen_ID': 32, 'plant_name': 'stiel_eiche'},
        }
        
    def download_data(self):
        for plant in self.plant_paths.keys():
            if plant == 'apfel_frueh':
                apfel_path = '/fruit/historical/PH_Jahresmelder_Obst_Apfel_1925_2020_hist.txt'
                apfel = pd.read_csv(self.root_path + apfel_path, sep = ';')
                apfel = apfel[apfel[' Referenzjahr'] < 1991]
                apfel_frueh = pd.read_csv(self.root_path + self.plant_paths[plant], sep = ';')
                apfel_frueh = apfel_frueh[apfel_frueh[' Referenzjahr'] >= 1991]
                apfel_complete = pd.concat((apfel, apfel_frueh), axis = 0)
                apfel_complete.to_csv(self.save_path + '{}.csv'.format(plant))
            else:
                pd.read_csv(self.root_path + self.plant_paths[plant], sep = ';').to_csv(self.save_path + '{}.csv'.format(plant))
        
    def load_data(self):
        for season in self.seasons.keys():
            
            df = pd.read_csv(self.save_path + '{}.csv'.format(self.seasons[season]['plant_name']))
            df.drop(['Unnamed: 0'], axis=1, inplace=True)
            df.columns = [x.replace(" ", "") for x in list(df.columns)]
            data = df[df.Phase_id == self.seasons[season]['Phasen_ID']]
            
            self.seasons[season]['mean'] = data.groupby(by="Referenzjahr")['Jultag'].mean()
            self.seasons[season]['mean'].rename(str(season), inplace = True)
            self.seasons[season]['median'] = data.groupby(by="Referenzjahr")['Jultag'].median()
            self.seasons[season]['median'].rename(str(season), inplace = True)
            self.seasons[season]['sd'] = data.groupby(by="Referenzjahr")['Jultag'].std()
            self.seasons[season]['sd'].rename(str(season), inplace = True)
            
            self.seasons[season]['data'] = data #.groupby(by="Referenzjahr")['Jultag'] .std()
            # self.seasons[season]['data'].rename(str(season), inplace = True)
            
            self.seasons[season]['count'] = (data['Referenzjahr'], data['Referenzjahr'].unique().shape[0]) 
            # self.seasons[season]['count'].rename(str(season), inplace = True)
            

    def aggregate_data(self, type_):
        if type_ == 'count':
            return [{x: self.seasons[x][type_]} for x in  self.seasons.keys()]
        else:
            agg_data = pd.concat([self.seasons[x][type_] for x in  self.seasons.keys()], axis=1, join='outer')
            return agg_data
