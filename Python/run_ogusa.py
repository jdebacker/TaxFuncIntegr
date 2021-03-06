# import ogusa
# import os
# import sys
# from multiprocessing import Process
import time

#OGUSA_PATH = os.environ.get("OGUSA_PATH", "../../ospc-dynamic/dynamic/Python")

#sys.path.append(OGUSA_PATH)

import postprocess
#from execute import runner # change here for small jobs
from execute import runner, runner_SS


def run_micro_macro(user_params):

    reform = {2017: {
        '_II_rt1': [.09],
        '_II_rt2': [.135],
        '_II_rt3': [.225],
        '_II_rt4': [.252],
        '_II_rt5': [.297],
        '_II_rt6': [.315],
        '_II_rt7': [0.3564],
        '_PT_rt1': [.09],
        '_PT_rt2': [.135],
        '_PT_rt3': [.225],
        '_PT_rt4': [.252],
        '_PT_rt5': [.297],
        '_PT_rt6': [.315],
        '_PT_rt7': [0.3564],
        '_STD': [[6350*2.0, 12700*2.0, 6350*2.0, 9350*2.0, 12700*2.0, 6350*2.0]],
        '_STD_Dep': [1050*2.0]
    }, }

    start_time = time.time()

    REFORM_DIR = "./OUTPUT_REFORM"
    BASELINE_DIR = "./OUTPUT_BASELINE"

    user_params = {'frisch': 0.41, 'start_year': 2017}

    '''
    --------------------------------------------------------------------
    Run SS for Baseline first - so can run baseline and reform in
    parallel if want
    --------------------------------------------------------------------
    '''
    # output_base = BASELINE_DIR
    # input_dir = BASELINE_DIR
    # kwargs={'output_base':output_base, 'baseline_dir':BASELINE_DIR,
    #         'baseline':True, 'analytical_mtrs':False, 'age_specific':True,
    #         'user_params':user_params,'guid':'int',
    #         'run_micro':True}
    # #p1 = Process(target=runner, kwargs=kwargs)
    # #p1.start()
    # runner_SS(**kwargs)


    '''
    --------------------------------------------------------------------
    Run baseline
    --------------------------------------------------------------------
    '''
    output_base = BASELINE_DIR
    input_dir = BASELINE_DIR
    kwargs={'output_base':output_base, 'baseline_dir':BASELINE_DIR,
            'baseline':True, 'analytical_mtrs':False, 'age_specific':True,
            'user_params':user_params,'guid':'int',
            'run_micro':False}
    #p1 = Process(target=runner, kwargs=kwargs)
    #p1.start()
    runner(**kwargs)
    # quit()

    '''
    --------------------------------------------------------------------
    Run reform
    --------------------------------------------------------------------
    '''
    output_base = REFORM_DIR
    input_dir = REFORM_DIR
    guid_iter = 'reform_' + str(0)
    kwargs={'output_base':output_base, 'baseline_dir':BASELINE_DIR,
            'baseline':False, 'analytical_mtrs':False, 'age_specific':True,
            'reform':reform, 'user_params':user_params,'guid':'int',
            'run_micro':False}
    #p2 = Process(target=runner, kwargs=kwargs)
    #p2.start()
    runner_SS(**kwargs)




    #p1.join()
    # print "just joined"
    #p2.join()

    # time.sleep(0.5)

    ans = postprocess.create_diff(baseline_dir=BASELINE_DIR,
        policy_dir=REFORM_DIR)

    print "total time was ", (time.time() - start_time)
    print ans

    return ans


if __name__ == "__main__":
    run_micro_macro(user_params={})
