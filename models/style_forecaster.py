import pandas as pd
import numpy as np
import os

class StyleForecaster:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.articles_df = pd.read_csv(os.path.join(data_dir, "articles.csv"))
        self.transactions_df = pd.read_csv(os.path.join(data_dir, "transactions_train.csv"))
        self.transactions_df['t_dat'] = pd.to_datetime(self.transactions_df['t_dat'])
        
        # Merge article metadata into transactions
        self.merged_df = self.transactions_df.merge(
            self.articles_df[['article_id', 'product_code', 'prod_name', 'product_type_name', 
                              'product_group_name', 'graphical_appearance_name', 
                              'colour_group_name', 'department_name', 'garment_group_name', 'detail_desc']],
            on='article_id',
            how='left'
        )
        
        # Add Season column based on month
        self.merged_df['month'] = self.merged_df['t_dat'].dt.month
        self.merged_df['season'] = self.merged_df['month'].map(self._map_season)
        
    def _map_season(self, month):
        if month in [3, 4, 5]: return 'Spring'
        elif month in [6, 7, 8]: return 'Summer'
        elif month in [9, 10, 11]: return 'Autumn'
        else: return 'Winter'

    def aggregate_styles(self):
        """
        Define a Style by combining key aesthetic and structural attributes:
        Garment Group + Product Type + Graphical Appearance + Primary Colour Group
        """
        df = self.merged_df.copy()
        df['style_key'] = (
            df['garment_group_name'] + " | " + 
            df['product_type_name'] + " | " + 
            df['graphical_appearance_name'] + " | " + 
            df['colour_group_name']
        )
        return df

    def predict_top_styles(self, season_filter=None, top_n=3):
        """
        Predict top performing styles based on multi-horizon momentum, velocity acceleration, and recent revenue.
        """
        df = self.aggregate_styles()
        
        if season_filter:
            df_target = df[df['season'] == season_filter].copy()
        else:
            df_target = df.copy()
            
        max_date = df_target['t_dat'].max()
        cutoff_recent = max_date - pd.Timedelta(weeks=12)
        cutoff_prior = cutoff_recent - pd.Timedelta(weeks=12)
        
        # Group by style_key
        style_groups = df_target.groupby(['style_key', 'garment_group_name', 'product_type_name', 
                                          'graphical_appearance_name', 'colour_group_name'])
        
        results = []
        for (style_key, g_group, p_type, graph, color), group in style_groups:
            total_units = len(group)
            total_revenue = (group['price']).sum()
            
            recent_group = group[group['t_dat'] >= cutoff_recent]
            prior_group = group[(group['t_dat'] >= cutoff_prior) & (group['t_dat'] < cutoff_recent)]
            
            recent_units = len(recent_group)
            prior_units = len(prior_group)
            recent_revenue = (recent_group['price']).sum()
            
            # Acceleration rate
            acceleration = (recent_units - prior_units) / max(prior_units, 1.0)
            
            # Representative sample articles
            sample_articles = group['article_id'].unique().tolist()
            sample_desc = group['detail_desc'].dropna().iloc[0] if len(group['detail_desc'].dropna()) > 0 else ""
            
            results.append({
                'style_key': style_key,
                'garment_group': g_group,
                'product_type': p_type,
                'graphical_appearance': graph,
                'colour_group': color,
                'total_units': total_units,
                'recent_units': recent_units,
                'prior_units': prior_units,
                'acceleration_pct': round(acceleration * 100, 2),
                'total_revenue': round(total_revenue, 2),
                'recent_revenue': round(recent_revenue, 2),
                'sample_articles': sample_articles,
                'detail_desc': sample_desc
            })
            
        res_df = pd.DataFrame(results)
        
        # Normalize metrics for composite scoring
        res_df['norm_recent_units'] = (res_df['recent_units'] - res_df['recent_units'].min()) / max((res_df['recent_units'].max() - res_df['recent_units'].min()), 1e-5)
        res_df['norm_acceleration'] = (res_df['acceleration_pct'] - res_df['acceleration_pct'].min()) / max((res_df['acceleration_pct'].max() - res_df['acceleration_pct'].min()), 1e-5)
        res_df['norm_revenue'] = (res_df['recent_revenue'] - res_df['recent_revenue'].min()) / max((res_df['recent_revenue'].max() - res_df['recent_revenue'].min()), 1e-5)
        
        # Composite Performance Score (PGS)
        res_df['composite_score'] = (
            0.40 * res_df['norm_recent_units'] +
            0.40 * res_df['norm_acceleration'] +
            0.20 * res_df['norm_revenue']
        )
        
        res_df = res_df.sort_values(by='composite_score', ascending=False).reset_index(drop=True)
        res_df['rank'] = res_df.index + 1
        
        return res_df.head(top_n), res_df
