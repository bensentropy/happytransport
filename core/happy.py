import math
# -*- coding: utf-8 -*-
"""
Created on Sat May 24 12:15:24 2014

@author: ben
"""

class HappyTravellerMetricsBS(object):
    
    health_calories_per_km = 76
    steps_height_multiplier=(1302-1616)/(1.83-1.47)
    steps_height_constant=1616 - (1302-1616)/(1.83-1.47)*1.47
    steps_target=10000
    met_values_by_speed={3.2:2.8,
                         4.0:3.0,
                         4.8:3.5,
                         5.6:4.3}
    #https://sites.google.com/site/compendiumofphysicalactivities/Activity-Categories/walking
    #http://www.livestrong.com/article/18303-calculate-calories-burned/
    #MET - 5.6 km/hr = brisk         = 4.3
    #MET - 4.8 km/hr = moderate  = 3.5 
    #MET - 4.0 km/hr = medium    = 3.0
    #MET - 3.2 km/hr = slow          = 2.8 
    days_per_week_travelled=5
    
    #http://en.wikipedia.org/wiki/Public_holidays_in_New_Zealand#Annual_leave_and_non-working_days
    work_weeks_per_year=46#52 weeks minus 4 weeks annual leave minus 10 public holidays
    
    cost_per_km_by_engine_size={'small':.532,'compact':.642,'medium':.788,'large':1.07}
    #http://www.aa.co.nz/assets/site-information/running-costs/2013-Petrol-Running-Costs.pdf?m=1378250354%22%20class=%22type:{pdf}%20size:{333%20KB}%20file

    #https://app.box.com/s/2sjky7olvt6ncelfvgjo
    car_carbon_emissions_petrol = (206.833426976629 + 208.968498458663)/2 #in grams
    car_carbon_emissions_diesel = (228.973097730254 + 230.184100865455)/2 #in grams
    car_pmex_petrol=(0.00461758705028405 + 0.00600007721608484)/2
    car_pmex_diesel=(0.190237091217936 + 0.242934304322229)/2

    trees_to_offset_one_tonne_CO2=6.667
    #http://carbon4good.yolasite.com/why-plant-trees.php 
    
    co2_social_cost_per_tonne_nzd=146
    #http://www.nature.com/nclimate/journal/v4/n4/full/nclimate2135.html 
    
    
    car_fuel_type=['petrol','diesel']
    
    
    #Long black = $3.5			[Starbucks]
    cost_coffee=3.5
    #Large hamburger combo = $10	[McDonnald]
    cost_hamburger_combo=10
    #Apple IPhone 5S = $1000		[PBTech]
    cost_apple_iphone_5S=1000
    #PS4 Console = $600			[JB-HiFi]
    cost_ps4=600
    #Amazon Best seller ebook = $10	[Amazon]
    cost_amazon_ebook=10

    

    #http://www.goodreads.com/poll/show/48965-reading-non-stop-how-long-does-it-take-you-to-read-a-300-page-book
    book_reading_time_hours=4.5
        
    def get_yearly_money_saving(self, daily_car_commute_km, daily_parking_cost, engine_size,daily_pt_cost):
        
        daily_car_travel_cost=self.cost_per_km_by_engine_size[engine_size]*daily_car_commute_km
        
        total_daily_car_cost=daily_parking_cost + daily_car_travel_cost
        
        total_yearly_car_cost = (
            total_daily_car_cost*
            self.days_per_week_travelled*
            self.work_weeks_per_year)
            
        total_yearly_pt_cost=(
            daily_pt_cost*
            self.days_per_week_travelled*
            self.work_weeks_per_year)
            
        total_savings=total_yearly_car_cost - total_yearly_pt_cost
        
        benefits = {}
        benefits['notes']={}
        
        benefits['total_amount']='${1:.{0}f}'.format(0,round(total_savings,0))
        benefits['coffees_each_week']=self.round_and_format(total_savings/52/self.cost_coffee)
        benefits['coffees_total']=self.round_and_format(total_savings/self.cost_coffee)
        benefits['hamburger_combos_total']=self.round_and_format(total_savings/self.cost_hamburger_combo)
        benefits['iphones_total']='{1:.{0}f}'.format(1,round(total_savings/self.cost_apple_iphone_5S,1))
        benefits['ps4_total']= self.round_and_format(math.floor(total_savings/self.cost_ps4))
        benefits['ebook_total']=self.round_and_format(total_savings/self.cost_amazon_ebook)
            
        return benefits
        
    def get_environmental_benefits(self,daily_car_commute_km,car_fuel_type='petrol',daily_bus_commute_km=0):
        yearly_car_commute_km=(
            daily_car_commute_km*
            self.days_per_week_travelled*
            self.work_weeks_per_year)

        carbon_emissions_car=0
        particle_emissions_car=0
        if(car_fuel_type=='petrol'):
            carbon_emissions_car = yearly_car_commute_km * self.car_carbon_emissions_petrol
            particle_emissions_car=yearly_car_commute_km * self.car_pmex_petrol
        else:
            carbon_emissions_car = yearly_car_commute_km * self.car_carbon_emissions_diesel
            particle_emissions_car=yearly_car_commute_km * self.car_pmex_diesel
        
        carbon_emissions_kg=carbon_emissions_car/1000
        carbon_emissions_tonne=carbon_emissions_kg/1000
        
        
        benefits = {}
        benefits['notes']={}
        benefits['links']={}
        
        benefits['carbon_emissions_kg']=self.round_and_format(carbon_emissions_kg)
        benefits['notes']['carbon_emissions_kg']='Carbon emissions from commuting via car over the year. Assumes a 2005 model car travelling at between 50 and 100 km/h.'
        benefits['links']['carbon_emissions_kg']='http://air.nzta.govt.nz/vehicle-emissions-prediction-model'
        
        benefits['carbon_emissions_tonne']='{1:.{0}f}'.format(1,round(carbon_emissions_tonne,1))
        
        benefits['carbon_emissions_social_cost']='${1:.{0}f}'.format(0,round(carbon_emissions_tonne*self.co2_social_cost_per_tonne_nzd,0))
        benefits['links']['carbon_emissions_social_cost'] = "http://www.nature.com/nclimate/journal/v4/n4/full/nclimate2135.html"
        benefits['notes']['carbon_emissions_social_cost'] = "Social cost in NZD"
        benefits['carbon_emissions_trees']=self.round_and_format(carbon_emissions_tonne*self.trees_to_offset_one_tonne_CO2)
        
        benefits['particle_emissions_car_grams']=self.round_and_format(particle_emissions_car)
        benefits['links']['particle_emissions_car_grams']='http://air.nzta.govt.nz/vehicle-emissions-prediction-model'
        benefits['notes']['particle_emissions_car_grams']='Particle emissions from commuting via car over the year in grams. Assumes a 2005 model car travelling at between 50 and 100 km/h.'
        
        benefits['links']="http://carbon4good.yolasite.com/why-plant-trees.php"
        return benefits
        
        
    
    def get_time_use_benefits(self,daily_car_use_hours,daily_pt_vehicle_hours,daily_pt_total_hours):
        """
        @param: daily_car_use_hours: time spend in the car per day (two-way) in hours
        @param: daily_pt_vehicle_hours: time spend in the PT vehicle (e.g., train, bus) (two-way) in hours
        @param: daily_pt_total_hours: total time spent in a PT journey (two-way)
        """
        yearly_pt_vehicle_hours = (
            self.work_weeks_per_year*
            self.days_per_week_travelled * 
            daily_pt_vehicle_hours
            )
        
        yearly_car_use_hours = (
            self.work_weeks_per_year*
            self.days_per_week_travelled * 
            daily_car_use_hours
            )
        #http://www.goodreads.com/poll/show/48965-reading-non-stop-how-long-does-it-take-you-to-read-a-300-page-book
        #it takes 3-6 hours for a 300 page book  according to
        benefits = {}
        
        benefits['notes']={}
        benefits['links']={}
        benefits['books_read']=self.round_and_format(yearly_pt_vehicle_hours/self.book_reading_time_hours)
        benefits['links']['books_read']="Goodreads.com poll. Retrieved from http://www.goodreads.com/poll/show/48965-reading-non-stop-how-long-does-it-take-you-to-read-a-300-page-book on 24 May 2014"
        
        
        benefits['yearly_car_use_hours']=self.round_and_format(yearly_car_use_hours)
        
        benefits['pt_one_way_commute_minutes']=self.round_and_format(float(daily_pt_total_hours)/2*60)
        
        return benefits
        
      
    
    
    def get_health_benefits(self,daily_km_walked,daily_walking_hours,weight_kg=85,height_m=1.71,walking_kph=4.0):
        """
        Gets health benefits from data
        benefits are:
        -steps walked
        -calories burned
        
        @param: km walked 
        @param: (optional) weight: (default is rounded-up kiwi average weight 81kg rounded up to 85kg) http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=10885815
        @param: (optional) height: (default is average kiwi height 1.71 m) http://en.wikipedia.org/wiki/Human_height#Average_height_around_the_world
        """
        benefits = {}
        
        benefits['notes']={}
        
        
        #CALORIES CALCULATOR
        #calories used = kg * METvalue * hours walking
        daily_cal=weight_kg * self.met_values_by_speed[walking_kph] * daily_walking_hours
        benefits['cals_burned'] = '{1:.{0}f}'.format(0,round(daily_cal,0))
        benefits['notes']['cals_burned_link'] = (
            "Compendium of Physical Activities, Health Lifestyles Research Center, School of Nutrition and Health, Arizona State University. Retrieved from https://sites.google.com/site/compendiumofphysicalactivities/contact-us on 24 May 2014\r\n"
            + "How to Calculate Calories Burned - Livestrong.com. Retrieved from http://www.livestrong.com/article/18303-calculate-calories-burned/ on 24 May 2014")
            
        #if (weight==None):
        #    benefits['calories'] = km_walked*57
        #else:
        #    benefits['notes']['calories']="Unfortunately we don't calculate cal/km by weight yet; this figure is based on a standard 85 kg weight"
        #    benefits['notes']['calories']=(benefits['notes']['calories'] 
        #        + "\r\nCalories based on burning " + 
        #        str(self.health_calories_per_km) 
        #        + " calories per km.")
        #    benefits['calories'] = km_walked*57
            
        #steps calculator
        #based on followign data from research:
        #x	y
        #height (m)	Steps
        #1.47	1616
        #1.83	1302
        #we use y=mx+c, steps = m*height+c
        #steps = -872.2222222222*height+2898.1666666667
        steps_per_km = self.steps_height_multiplier*height_m + self.steps_height_constant
        steps_walked = steps_per_km*daily_km_walked
        benefits['steps']='{1:.{0}f}'.format(0,round(steps_walked,0))
        benefits['steps_percent_target']='{1:.{0}f}%'.format(0,round(steps_walked/self.steps_target*100,0))
        benefits['notes']['steps']="US Health Authority boffins recommend you walk 10000 steps a day to become a star olympic athlete!"
        benefits['notes']['steps_link']="http://www.nhs.uk/Livewell/loseweight/Pages/10000stepschallenge.aspx"
        
        
        return benefits
        
    def round_and_format(self,x):
        return '{1:.{0}f}'.format(0,round(x,0))