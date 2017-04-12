from poll_uscis import *
import numpy as np
from time import sleep
import sys

if __name__ == '__main__':
	#for i in range(100):
	#	print np.random.poisson(10.0)
	#sys.exit(0)
	num_queries = int(sys.argv[1])
	start = 121401
	D = {}
	for n in range(start, start+num_queries):
		case_number = 'YSC1790%d' % n
		code, status, detail = poll_optstatus(case_number)
		if code == STATUS_ERROR:
			print 'The case number %s is invalid.' % case_number
		else:
			if status in D:
				D[status] += 1
			else:
				D[status] = 1
			# report format
			report_format = ("-------  Your USCIS Case [{0}]---------"
							 "\nCurrent Status: [{1}]"
							 "\nDays since received: [{2}]")
			try:
				days_elapsed = get_days_since_received(detail)
			except Exception as e:
				pass
			finally:
				days_elapsed = -1

			report = report_format.format(case_number, status, days_elapsed)
			# compare with last status
			changed, laststatus = on_status_fetch(status, case_number)
			# generate report
			report = '\n'.join(
				[report, "Previous Status:%s \nChanged?: %s" % (laststatus, changed),
				 "Current Timestamp: %s " % datetime.now().strftime("%Y-%m-%d %H:%M")])
			print '[%s] %s' % (case_number, status)
			#print report
			sleep_time = np.random.poisson(10) * 0.1
			print 'sleeping for %d s' % sleep_time
			sleep(sleep_time)			
	print D
