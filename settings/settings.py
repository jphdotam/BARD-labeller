settings = {

    "Accessory Pathway":{
        'type': '12lead',
        'ranges': {
            'sinus pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'sinus qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'sinus twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'hra paced pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'hra paced qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'hra paced twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'cs paced pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'cs paced qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'cs paced twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'rr': {
                'text': 'RR interval',
                'mandatory': True,
                'minmax': [200, 3000]
            },
            'post-ablation pwave': {
                'text': 'Sinus P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'post-ablation qrs': {
                'text': 'Sinus QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'post-ablation twave': {
                'text': 'Sinus T wave',
                'mandatory': False,
                'minmax': [20, 800]
            }
        },
        'markers':{
            'deltawave end': {
                'text': 'End of delta wave',
                'mandatory': True
            },
            'deltawave inner deflection': {
                'text': 'Inner deflection within delta wave',
                'mandatory': False
            }
        },
        'labels': {
            # These are labels for the entire loaded file, individual labels for ranges nested within the range entries
            'prepostablation': {
                'text': "Is the patient pre- or post-ablation?",
                'options': ['pre', 'post'],
                'default': 'pre',
                'mandatory': True
            }
        }
    },


    "Ventricular Ectopy":{
        'type': '12lead',
        'ranges': {
            # Minimum and maximum in ms
            'ectopic qrst': {
                'text': 'Ectopic QRS-T complex\nRemember to include the T wave!',
                'mandatory': True,
                'minmax': [120, 400],
                'labels': {
                    # Labels for this specific range
                    'identity': {
                        'text': "What ID # is this ectopic",
                        'options': ['intrinsic','paced','catheter'],
                        'mandatory': True
                    }
                }
            },
            'sinus pwave': {
                'text': 'Sinus P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'sinus qrs': {
                'text': 'Sinus QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'sinus twave': {
                'text': 'Sinus T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'rr': {
                'text': 'Preceding RR interval',
                'mandatory': False,
                'minmax': [200, 3000]
            },
            'rv': {
                'text': 'RV interval',
                'mandatory': False,
                'minmax': [200, 3000]
            }
        },
        'markers': {
            't onset': {
                'text': 'Onset of ectopic T wave',
                'mandatory': True
            },
            'pacing spike': {
                'text': 'Location of pacing spike',
                'mandatory': False
            }
        },
        'labels': {
            # These are labels for the entire loaded file, individual labels for ranges nested within the range entries
            'location': {
                'text': "What is the location of the ectopic?",
                'options': ['lvot','rvot','other'],
                'mandatory': False
            }
        }
    },

"Accessory Pathway":{
        'type': '12lead',
        'ranges': {
            # Minimum and maximum in ms
            'sinus pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'sinus qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'sinus twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'hra paced pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'hra paced qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'hra paced twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'cs paced pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'cs paced qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'cs paced twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'rr': {
                'text': 'RR interval',
                'mandatory': True,
                'minmax': [200, 3000]
            },
            'post-ablation pwave': {
                'text': 'Sinus P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'post-ablation qrs': {
                'text': 'Sinus QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'post-ablation twave': {
                'text': 'Sinus T wave',
                'mandatory': False,
                'minmax': [20, 800]
            }
        },
        'markers':{
            'deltawave end': {
                'text': 'End of delta wave',
                'mandatory': True
            },
            'deltawave inner deflection': {
                'text': 'Inner deflection within delta wave',
                'mandatory': False
            }
        },
        'labels': {
            # These are labels for the entire loaded file, individual labels for ranges nested within the range entries
            'prepostablation': {
                'text': "Is the patient pre- or post-ablation?",
                'options': ['pre', 'post'],
                'default': 'pre',
                'mandatory': True
            }
        }
    },
    "AVNRT":{
        'type': '12lead',
        'ranges': {
            # Minimum and maximum in ms
            'sinus pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'sinus qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'sinus twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'hra paced pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'hra paced qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'hra paced twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'cs paced pwave': {
                'text': 'P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'cs paced qrs': {
                'text': 'QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'cs paced twave': {
                'text': 'T wave',
                'mandatory': False,
                'minmax': [20, 800]
            },
            'rr': {
                'text': 'RR interval',
                'mandatory': True,
                'minmax': [200, 3000]
            },
            'post-ablation pwave': {
                'text': 'Sinus P wave',
                'mandatory': False,  # Might be in AF
                'minmax': [40, 200]
            },
            'post-ablation qrs': {
                'text': 'Sinus QRS complex',
                'mandatory': False,
                'minmax': [40, 400]
            },
            'post-ablation twave': {
                'text': 'Sinus T wave',
                'mandatory': False,
                'minmax': [20, 800]
            }
        },
        'markers':{
            'pseudodelta wave end': {
                'text': 'End of pseudodelta wave',
                'mandatory': False
            }
        },
        'labels': {
            # These are labels for the entire loaded file, individual labels for ranges nested within the range entries
            'prepostablation': {
                'text': "Is the patient pre- or post-ablation?",
                'options': ['pre', 'post'],
                'default': 'pre',
                'mandatory': True
            }
        }
    }
}