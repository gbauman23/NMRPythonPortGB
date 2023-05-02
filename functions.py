# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:12:55 2023

@author: pguest
"""

import nidaqmx
import nidaqmx.system
import nidaqmx.constants as NIconst
import time
import numpy as np
import matplotlib.pyplot as plt

def NIDAQ_diagnostics():
    # Print Device List for diagnostics
    system = nidaqmx.system.System.local()
    for device in system.devices:
        print(device)


def SingleRead():
    """
        Ultra-simple read, but limited to 700Hz
    """
    device = 'Dev1'
    with nidaqmx.Task() as task1:    
        task1 = nidaqmx.Task()
        task1.ai_channels.add_ai_voltage_chan(f"{device}/ai2")
        task1.ai_channels.add_ai_voltage_chan(f"{device}/ai0")
        task1.start()
        value = task1.read()
        print(value)
        task1.stop()
        task1.close()
        return value

def AI_example_nidaqmx():
    """
        Example of analog input on 2 channels.
        Using "with" insures that everything gets cleaned up afterward.  The "as" just makes a shorthand.
        Set up channels (channel, min, and max are probably useful), then set up timing rate.  the read call sends the trigger.
        For unhelpful help see "https://nidaqmx-python.readthedocs.io/en/latest/start_trigger.html"
        Use NI-MAX (Natl. Inst. Meas. and Automation eXplorer) to find the device name on your system. 
        Commented lines at the end give other parameters that can be controled
    """
    with nidaqmx.Task() as task1:                                                                               # using "with" insures that everything gets cleaned up at the end
        task1.ai_channels.add_ai_voltage_chan("Dev1/ai0", \
            name_to_assign_to_channel="AI0",terminal_config=NIconst.TerminalConfiguration.DEFAULT, \
            min_val=-10, max_val=10, units = NIconst.VoltageUnits.VOLTS)                                        # full assignment
        task1.ai_channels.add_ai_voltage_chan("Dev1/ai1")                                                       # Minimal assignment
        task1.timing.cfg_samp_clk_timing(rate=1000)
        
        data0,data1 =task1.read(number_of_samples_per_channel = 50,timeout=10.0)
        print(data0,data1)
        return data0, data1
        #print("\tmax sample rate = ", task1.timing.ai_conv_max_rate, "\t sample rate set to: ",task1.timing.ai_conv_rate )
        #task.cfg_samp_cl_timing(samplerate, source='',activ_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE,samps_per_chan=Nsamples)
                #print(nidaqmx.constants.TerminalConfiguration.PSEUDODIFFERENTIAL, nidaqmx.constants.TerminalConfiguration.DEFAULT)
        #print(task1.timing, task1.triggers)
        #task1.timing.cfg_samp_clk_timing(rate=100,sample_mode=NIconst.AcquisitionType.FINITE,samps_per_chan=40)


    
def AO_example_nidaqmx():
    """
        Example of analog output on 2 channels.
        Using "with" insures that everything gets cleaned up afterward.  The "as" just makes a shorthand.
        Set up channels, then set up timing rate.  the write call sends the trigger.
        You need "samps_per_chan", otherwise it doesn't think it has ever finished.'
        AcquisitionType FINITE returns immediately and requires wait_until_done() and stop().  If left blank (On Demand), the return is delayed until the task is finished.
        Output continuously cycles through the data you give in "write" until it has reached "samps_per_chan"
        For unhelpful help see "https://nidaqmx-python.readthedocs.io/en/latest/start_trigger.html"
        Use NI-MAX (Natl. Inst. Meas. and Automation eXplorer) to find the device name on your system. 
        Commented lines at the end give other parameters that can be controled
    """
    with nidaqmx.Task() as task2:
        task2.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        #task2.ao_channels.add_ao_voltage_chan("Dev1/ao1")
        task2.timing.cfg_samp_clk_timing(rate=1, samps_per_chan=2)
        task2.write([2.7,1],auto_start=True,timeout=10.0)
        task2.wait_until_done()
        task2.stop()
        
        #task2.timing.cfg_samp_clk_timing(rate=1,sample_mode=NIconst.AcquisitionType.FINITE,samps_per_chan=2)
        #task2.start_trigger.cfg_dig_edge_start_trig(trigger_source = "/Dev1/ai/StartTrigger")
        #task2.triggers.start_trigger.delay_units(NIconst.DigitalWidthUnits.SECONDS)
        #task2.triggers.start_trigger.delay(0.1)
        
def setMagnetField(val):
    with nidaqmx.Task() as task2:
        task2.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        #task2.timing.cfg_samp_clk_timing(rate=1, samps_per_chan=2)
        #task2.write([val,val],auto_start=True,timeout=10.0)
        task2.write(val, auto_start=True, timeout = 10.0)
        task2.wait_until_done()
        task2.stop()



def DO_example_nidaqmx():
    if (0):
        print("task3")
        with nidaqmx.Task() as task3, nidaqmx.Task() as task5:
            task3.co_channels.add_co_pulse_chan_time("Dev1/ctr1", low_time = 0.01, high_time=0.01)
            task3.timing.cfg_implicit_timing(sample_mode=NIconst.AcquisitionType.FINITE,samps_per_chan=5)
            task3.start()
            #sample = nidaqmx.types.CtrTime(high_time=0.1, low_time=0.1)
            #print(task3.write(sample))
    if (0):
        with nidaqmx.Task() as task6:
            task6.do_channels.add_do_chan("Dev1/port0/line5")
            print(task6.write([True]))
            time.sleep(1)
            print(task6.write([False]))
    if (1):
        # DOES NOT WORK
        with nidaqmx.Task() as task6, nidaqmx.Task() as task7:
            task6.do_channels.add_do_chan("Dev1/port0/line5")
            task6.timing.cfg_samp_clk_timing(rate=10, source="/Dev1/ctr1internaloutput", samps_per_chan=3) 
            #task6.timing.cfg_samp_clk_timing(rate=10, source="/Dev1/ai/SampleClock", samps_per_chan=3) 
            
            task7.co_channels.add_co_pulse_chan_time("Dev1/ctr1", low_time=1, high_time=1)
            task7.timing.cfg_implicit_timing(sample_mode=NIconst.AcquisitionType.CONTINUOUS)
            task7.start()

            print(task6.write([True,False,True]))
            task6.wait_until_done(timeout = 6)
            #time.sleep(1)
            #print(task6.write([False,True,False]))
    if (0):
        print("task4")
        with nidaqmx.Task() as task4, nidaqmx.Task() as task5:
            task4.do_channels.add_do_chan("Dev1/port0/line5")
            #task4.do_channels.add_do_chan("Dev1/port0/line4")
            task4.timing.cfg_samp_clk_timing(rate=1, source="/Dev1/ai/SampleClock",samps_per_chan=3)            #rate must be present but is set by ai
            
            #task4.timing.cfg_samp_clk_timing(rate=1,sample_mode=NIconst.AcquisitionType.FINITE,samps_per_chan=4)
            #task4.timing.cfg_implicit_timing()
            print(task4.write([True,False,True],auto_start=True,timeout=5.0))
            
            task5.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            task5.timing.cfg_samp_clk_timing(rate=10)
            print(task5.read(number_of_samples_per_channel=10,timeout=10.0))
            
            #task4.wait_until_done()
            #task4.stop()
     



def mixed_example_nidaqmx():
    """
        Example of mixed AI and AO with the start of the AO triggered by the AI.
        Using "with" insures that everything gets cleaned up afterward.  The "as" just makes a shorthand.
        AI: set up channels, then set up timing rate
        AO: set up channels, then set up timing rate and samps_per_channel.   You need "samps_per_chan", otherwise it doesn't think it has ever finished.'
        AcquisitionType FINITE returns immediately and requires wait_until_done() and stop().  If left blank (On Demand), the return is delayed until the task is finished.
        Output continuously cycles through the data you give in "write" until it has reached "samps_per_chan"
        Then set AO trigger to the AI start trigger
        the write does not pull the trigger, but the read does.
        For unhelpful help see "https://nidaqmx-python.readthedocs.io/en/latest/start_trigger.html"
        Use NI-MAX (Natl. Inst. Meas. and Automation eXplorer) to find the device name on your system. 
        Commented lines at the end give other parameters that can be controled
        Master/Slave does not seem to work on E series boards.
    """
    with nidaqmx.Task() as task1, nidaqmx.Task() as task2:
        task1.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        task1.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        task1.timing.cfg_samp_clk_timing(rate=5e5)
    
        task2.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task2.ao_channels.add_ao_voltage_chan("Dev1/ao1")
        task2.timing.cfg_samp_clk_timing(rate=5e5, source="/Dev1/ai/sampleclock", samps_per_chan=4)
        task2.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/ai/StartTrigger")
    
        task2.write([[0.5,1.0,1.5,2.0],[2.5,3.0,3.5,4.0]],auto_start=True,timeout=10.0)
        print(task1.read(number_of_samples_per_channel=6,timeout=10.0))

        #task1.triggers.sync_type.MASTER = True
        #task2.triggers.sync_type.SLAVE = True
        #task1.control(TaskMode.TASK_COMMIT)
        #task2.timing.cfg_samp_clk_timing(rate=1,source="PFI0",sample_mode=NIconst.AcquisitionType.FINITE,samps_per_chan=2)
        #task2.timing.cfg_samp_clk_timing(rate=5e5,sample_mode=NIconst.AcquisitionType.FINITE ,samps_per_chan=4)
        #task2.wait_until_done()
        #task1.wait_until_done()
        #time.sleep(2.5)
        #task2.stop()
        #task1.stop()
        #print(nidaqmx.errors.DaqError("dd",200010))
        
        

def FIDpulse(pulse_frequency=35000, pulse_width=0.001, pulse_amplitude=0.5, mute_time=0.0005, readout_time=0.1):
    #typical: pulse_frequency=35000, pulse_width=0.001, pulse_amplitude=0.5, mute_time=0.0005, readout_time=0.1
    AO_Sample_Frequency = 1e5  #9e5
    AI_Sample_Frequency = 1e5
    print("FIDpulse:  pulse_frequency= ",pulse_frequency,"pulse_width= ", pulse_width,"pulse_amplitude= ",pulse_amplitude)

    # AI number of points
    ai_N = int(np.round(AI_Sample_Frequency*readout_time))
    ai_t = np.linspace(0,readout_time, int(ai_N))

    # make AO output
    ao_totaltime = 1.1*(pulse_width + mute_time)                        #extra time to insure a stretch of 0 at the end
    ao_N = np.round(AO_Sample_Frequency * ao_totaltime)
    ao_t = np.linspace(0,ao_totaltime, int(ao_N))
    ao_V=pulse_amplitude *np.sin(pulse_frequency*2.0*np.pi*ao_t)
    ao_V = ao_V * (ao_t<=pulse_width)                                   #set output to 0 after pulse
    if (1):                                                              #round off end of pulse to avoid sharp edge.  
        tail = 0.02                                                        #fraction of end to round off
        for i in range(0,int(0.02*ao_N),1):                                
            ao_V[-i] = ao_V[-i] * (1-np.exp(-3*i/10))                       #how fast to round off.
    
    #make DO signals:  pulse and mute
    do_totaltime = 1.1*(pulse_width + mute_time)                        #extra time to insure a stretch of 0 at the end
    do_N = int(np.round(AI_Sample_Frequency*do_totaltime))
    do_t = np.linspace(0,do_totaltime, int(do_N))
    do_pulse=(do_t <= pulse_width)
    do_mute=(do_t <= pulse_width + mute_time)

    if (1):     # Show plot of pulses
        plt.figure("Pulse Timing")
        plt.clf()
        plt.plot(ao_t, ao_V,'r-+')
        plt.plot(do_t, do_pulse,'g-')
        plt.plot(do_t, do_mute,'b-')
        print("frog")
        plt.show()

    with nidaqmx.Task() as task_ai, nidaqmx.Task() as task_ao, nidaqmx.Task() as task_do:
        task_ai.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        task_ai.timing.cfg_samp_clk_timing(rate=AI_Sample_Frequency)
    
        task_ao.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task_ao.timing.cfg_samp_clk_timing(rate=AO_Sample_Frequency, source="/Dev1/ai/sampleclock", samps_per_chan=do_N)
        task_ao.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/ai/StartTrigger")
    
        task_ao.write(ao_V,auto_start=True,timeout=10.0)
        data = task_ai.read(number_of_samples_per_channel=ai_N,timeout=10.0)
        task_ai.wait_until_done()
        
    
    print("ai_N= ", ai_N, "len(data)=", len(data))

    if (1):     # Show plot of pulses
        plt.figure("Data")
        plt.clf()
        plt.plot(ai_t, data,'r-')
        plt.show()
        
        
if __name__ == "__main__":
    NIDAQ_diagnostics()
    AO_example_nidaqmx()
    
#    start = time.monotonic()
#    device = 'Dev2'
#    with nidaqmx.Task() as task1:    
#        task1 = nidaqmx.Task()
#        task1.ai_channels.add_ai_voltage_chan(f"{device}/ai2")
#        task1.ai_channels.add_ai_voltage_chan(f"{device}/ai1")
#        task1.start()
#        value = task1.read()
#        #print(value)
#        #task1.stop()
#
#        for i in range(700): 
#            
#            value = task1.read()
#            #time.sleep(0.1)
#        end = time.monotonic()-start
#        
#        task1.stop()
#    print (end)
    
    #mixed_example_nidaqmx()
    #AO_example_nidaqmx()
    #DO_example_nidaqmx()
    #FIDpulse(pulse_frequency=3000, pulse_width=0.001, pulse_amplitude=0.5, mute_time=0.0002, readout_time=0.01)
