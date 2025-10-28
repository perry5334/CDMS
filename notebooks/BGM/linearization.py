import numpy as np

'''
Simple class to perform the linearization on data.
'''
class linearization:
    def __init__(self,
                det,
                E_est,
                binType = 'unbinned'):

        # a and b taken from this page
        ## https://confluence.slac.stanford.edu/spaces/CDMS/pages/573784925/Linearization+of+energy+scale+Ge+50+V#det-2841
        a = {
            1:{
                'PTOFamps':{
                    'binned':3.825e-04,
                    'unbinned':2.08e-04
                },
                'Psum':{
                    'binned':3.49e-04,
                    'unbinned':1.88e-04
                },
                'nxmPsum':{
                    'binned':2.73e-04,
                    'unbinned':1.56e-04
                }
            },
            3:{
                'PTOFamps':{
                    'binned':3.77e-04,
                    'unbinned':2.26e-04
                },
                'Psum':{
                    'binned':3.14e-04,
                    'unbinned':2.23e-04
                },
                'nxmPsum':{
                    'binned':1.84e-04,
                    'unbinned':1.40e-04
                }    
            }
        }
        
        b = {
            1:{
                'PTOFamps':{
                    'binned':8.55,
                    'unbinned':1.63e+01
                },
                'Psum':{
                    'binned':1.02e+01,
                    'unbinned':1.98e+01
                },
                'nxmPsum':{
                    'binned':1.23e+01,
                    'unbinned':2.27e+01
                }
            },
            3:{
                'PTOFamps':{
                    'binned':9.97,
                    'unbinned':1.75e+01
                },
                'Psum':{
                    'binned':1.31e+01,
                    'unbinned':1.92e+01
                },
                'nxmPsum':{
                    'binned':2.18e+01,
                    'unbinned':3.02e+01
                }    
            }
        }
        self.a = a[det][E_est][binType]
        self.b = b[det][E_est][binType]

    def exp(self, x):
        return (np.exp(x/self.a) - 1)/self.b

    def log(self, x):
        return self.a*np.log(x*self.b+1)
        
    def linearize(self, amps):
        lin_amps = self.exp(amps)
        return lin_amps
    
    def unlinearize(self, lin_amps):
        amps = self.log(lin_amps)
        return amps

    def CalibFactorConvert(self, LinCalibFactor, LinAmp):
        dAmpdLinAmp = (self.a * self.b)/(LinAmp * self.b + 1)
        return LinCalibFactor * (1/dAmpdLinAmp)
        