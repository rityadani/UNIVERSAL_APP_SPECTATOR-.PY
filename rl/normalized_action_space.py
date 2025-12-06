"""
Normalized Action Space - Universal action taxonomy across all apps
"""

class NormalizedActionSpace:
    """
    Unified action taxonomy that works across all application types.
    Maps app-specific actions to universal action categories.
    """
    
    # Universal action categories
    UNIVERSAL_ACTIONS = {
        'RESTART': {
            'category': 'restart',
            'description': 'Restart the application/service',
            'risk_level': 'medium',
            'aliases': ['restart_service', 'restart_django', 'restart_fastapi', 
                       'restart_nextjs', 'restart_spring', 'restart_container', 
                       'restart_dev_server']
        },
        'SCALE': {
            'category': 'scale',
            'description': 'Scale application resources',
            'risk_level': 'safe',
            'aliases': ['scale_up', 'scale_down', 'change_replica_count']
        },
        'CLEAR_CACHE': {
            'category': 'clear_cache',
            'description': 'Clear application cache',
            'risk_level': 'safe',
            'aliases': ['clear_cache', 'clear_next_cache', 'clear_node_modules']
        },
        'REBUILD': {
            'category': 'rebuild',
            'description': 'Rebuild application',
            'risk_level': 'medium',
            'aliases': ['rebuild_project', 'rebuild_app', 'rebuild_image']
        },
        'REDEPLOY': {
            'category': 'redeploy',
            'description': 'Redeploy application',
            'risk_level': 'high',
            'aliases': ['redeploy', 'deploy']
        },
        'HEALTH_CHECK': {
            'category': 'health_check',
            'description': 'Check application health',
            'risk_level': 'safe',
            'aliases': ['check_health', 'health_check', 'ping']
        },
        'ROLLBACK': {
            'category': 'rollback',
            'description': 'Rollback to previous version',
            'risk_level': 'high',
            'aliases': ['rollback', 'revert']
        },
        'RELOAD': {
            'category': 'reload',
            'description': 'Reload application configuration',
            'risk_level': 'safe',
            'aliases': ['reload_app', 'reload', 'hot_reload']
        }
    }
    
    def __init__(self, app_spec):
        self.app_spec = app_spec
        self.app_actions = app_spec.get('available_actions', [])
        self.normalized_map = self._build_normalized_map()
    
    def _build_normalized_map(self):
        """Map app-specific actions to universal categories"""
        mapping = {}
        
        for action in self.app_actions:
            action_name = action['name']
            
            # Find matching universal category
            for universal_action, details in self.UNIVERSAL_ACTIONS.items():
                if action_name in details['aliases']:
                    mapping[action_name] = {
                        'universal_category': universal_action,
                        'original_action': action,
                        'normalized_name': details['category'],
                        'risk_level': action.get('risk_level', details['risk_level'])
                    }
                    break
            
            # If no match, keep original
            if action_name not in mapping:
                mapping[action_name] = {
                    'universal_category': 'CUSTOM',
                    'original_action': action,
                    'normalized_name': action_name,
                    'risk_level': action.get('risk_level', 'medium')
                }
        
        return mapping
    
    def get_normalized_actions(self):
        """Get list of normalized action names"""
        return [details['normalized_name'] for details in self.normalized_map.values()]
    
    def get_universal_category(self, action_name):
        """Get universal category for an action"""
        return self.normalized_map.get(action_name, {}).get('universal_category', 'CUSTOM')
    
    def get_equivalent_actions(self, universal_category):
        """Get all app actions that map to a universal category"""
        return [
            action_name 
            for action_name, details in self.normalized_map.items() 
            if details['universal_category'] == universal_category
        ]
    
    def is_safe_action(self, action_name):
        """Check if action is safe to execute"""
        action_info = self.normalized_map.get(action_name, {})
        return action_info.get('risk_level', 'medium') == 'safe'
    
    def get_action_taxonomy(self):
        """Get complete action taxonomy for this app"""
        taxonomy = {}
        
        for universal_action in self.UNIVERSAL_ACTIONS.keys():
            equivalent = self.get_equivalent_actions(universal_action)
            if equivalent:
                taxonomy[universal_action] = equivalent
        
        return taxonomy

def normalize_action_across_apps(action_name, source_app_spec, target_app_spec):
    """
    Translate an action from one app to equivalent action in another app.
    Enables RL to transfer knowledge across different applications.
    """
    source_space = NormalizedActionSpace(source_app_spec)
    target_space = NormalizedActionSpace(target_app_spec)
    
    # Get universal category of source action
    universal_category = source_space.get_universal_category(action_name)
    
    # Find equivalent action in target app
    equivalent_actions = target_space.get_equivalent_actions(universal_category)
    
    if equivalent_actions:
        return equivalent_actions[0]  # Return first equivalent
    
    return None  # No equivalent action found

# Example usage
if __name__ == "__main__":
    import json
    
    # Test with Flask backend
    with open('../spec/example_app_spec.json', 'r') as f:
        flask_spec = json.load(f)
    
    flask_space = NormalizedActionSpace(flask_spec)
    
    print("Flask Backend - Normalized Actions:")
    print(flask_space.get_normalized_actions())
    
    print("\nAction Taxonomy:")
    print(flask_space.get_action_taxonomy())
    
    print("\nUniversal Categories:")
    for action in flask_spec['available_actions']:
        category = flask_space.get_universal_category(action['name'])
        print(f"{action['name']} → {category}")