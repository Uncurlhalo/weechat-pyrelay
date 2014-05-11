import relay
import weechatObjects as objs

def processReply(self, reply, buffers):
	# this will take the reply, look at is ID field, and take some action based on its type
	# these actions will all update weechat datastructures from weechatObjects.
	options = {	'_buffer_opened' : bufOpened,
				'_buffer_moved' : bufMoved,
				'_buffer_merged' : bufMerged,
				'_buffer_unmerged' : bufUnmerged,
				'_buffer_hidden' : bufHidden,
				'_buffer_unhidden' : bufUnhidden,
				'_buffer_renamed' : bufRenamed,
				'_buffer_title_changed' : bufTitleChanged,
				'_buffer_type_changed' : bufTypeChanged,
				'_buffer_localvar_added' : bufLocVarAdded,
				'_buffer_localvar_changed' : bufLocVarChanged,
				'_buffer_localvar_removed' : bufLocVarRemoved,
				'_buffer_line_added' : bufLineAdded,
				'_buffer_closing' : bufClosing,
				'_nicklist' : nicklist,
				'_nicklist_diff' : nicklistDiff,
				'_pong' : pong,
				'_upgrade' : upgrade,
				'_upgrade_ended' : upgradeEnded
				}
	msgID = reply.msgID
	otpions[msgID](reply, buffers)

def bufLineAdded(self, reply, buffers):
	replyItems = reply.objects[0].value['items']
	for key,buf in buffers:
		if buf.path == replyItems['buffer']:
			for item in replyItems:
				displayed = bool(item['displayed'])
				message = item['message']
				prefix = item['prefix']
				date = item['date']
			buf.lines.append(objs.WeechatLine(message, date, prefix, displayed))