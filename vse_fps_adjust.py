bl_info = {
	"name": "Movie clip Time to FPS",
	"author": "escape_code",
	"version": (1, 0),
	"blender": (2, 76, 0),
	"location": "Sequencer > Strip",
	"description": "Automatically wrap selected strips into meta with movie speed adjust to scene FPS\nBlender is FPS based not seconds based (like movies are).  This add-on handles the conversion.\n  Exiftool is needed on your computer to use this add-on (e.g. apt-get install libimage-exiftool-perl_8.60-2), http://www.sno.phy.queensu.ca/~phil/exiftool/, https://smarnach.github.io/pyexiftool/ and rename to exiftool.exe or exiftool and put in C:\Windows or /usr/bin, etc. put exiftool.py in blender/2.7x/python/lib/ or other lib folder\n Also panel put under 'Render' properties section.  https://developer.blender.org/diffusion/BAC/browse/master/sequencer_extra_actions/",
	"warning": "Meta functionality still being worked on.  Speed effect has a multiply speed argument with only a precision to .00",
	"wiki_url": "http://localhost/",
	"category": "Sequencer"
}

import bpy

try:	# TODO: add feature to alert/install exiftool and exiftool.py
	import exiftool
except ImportError:
	sys.exit(0)
# --------------------------
bpy.types.Scene.use_VSEfps = bpy.props.BoolProperty(	# TODO: move to a valid key location
    name="VSE to FPS",
    description="adjust VSE video clip's FPS to match output FPS",
    default=False
)

def RenderVSEPanelAdd(self, context):
	layout = self.layout
	row = layout.row()
	#row.label(text="hi")
	row.prop(bpy.context.scene, "use_VSEfps")

bpy.types.RENDER_PT_dimensions.append(RenderVSEPanelAdd)

# --------------------------

from bpy.types import Menu, Panel

def pollHandler(scene):
	checkFPS()

	#if bpy.ops.sequencer.movie_strip_add.poll() is True:
		#print("yipee")

bpy.app.handlers.scene_update_post.append(pollHandler)	# FIXME: maybe use a better trigger/polling mechanism

# --------------------------
bpy.types.Scene.last_FPS = bpy.context.scene.render.fps

def checkFPS():
	if bpy.context.scene.use_VSEfps == True and bpy.context.scene.render.fps != bpy.types.Scene.last_FPS:
		print("\n**** FPS changed to " + str(bpy.context.scene.render.fps))
		bpy.types.Scene.last_FPS = bpy.context.scene.render.fps

		if hasattr(bpy.context.scene.sequence_editor, "sequences"):
			# for i in bpy.context.scene.sequence_editor.sequences:
			#	print("metastrip " . i.name)
			updateAllMetas()

# used for making strip menu option
class MovieTimeToFPS(bpy.types.Operator):
	"""Wrap selected strips in meta with movie strip speed adjusted to scene FPS"""	  # blender will use this text as a tooltip for menu items and buttons (which in not language normalized)
	bl_idname = "sequencer.movietofpsmeta"		# unique identifier for buttons and menu items to reference.
	bl_label = "Movie Time to FPS meta"		 # display name in the interface.
	#bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
	bl_space_type = "SEQUENCE_EDITOR"
	bl_region_type = 'WINDOW'
	#bl_context = "object"

	def execute(self, context):		# execute() is called by blender when running the operator.
		# check to make sure exiftool works
		print("MovieTimeToFPS")
		createSpeedMeta(bpy.context.selected_sequences)

		return {'FINISHED'}			# this lets blender know the operator finished successfully.


class VSEtoFPSPanel(bpy.types.Panel):
	"""Creates a new Panel in the Render properties tab"""
	bl_label = "VSE FPS sync"
	bl_idname = "RENDER_PT_VSEtoFPS"
	bl_options = {'DEFAULT_CLOSED'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"
	last_FPS = bpy.context.scene.render.fps

	my_bool = bpy.props.BoolProperty(name="Toggle Option")

	def draw(self, context):
		# print (context.scene.render.fps)

		layout = self.layout
		row = layout.row()
		row.label(text="FPS: " + str(context.scene.render.fps), icon='WORLD_DATA')

		row = layout.row()
		#row.prop(context.scene.render, "fps")
		#row.prop(context.scene.render, "VSEtoFPSPanel")
		row.prop(bpy.context.scene, "use_VSEfps")

		scn = context.scene

		# if bpy.context.scene.render.fps != self.last_FPS:
			# print("FPS changed to " + str(bpy.context.scene.render.fps))
			# self.last_FPS = bpy.context.scene.render.fps
#
			# if hasattr(bpy.context.scene.sequence_editor, "sequences"):
				# # for i in bpy.context.scene.sequence_editor.sequences:
				# #	print("metastrip " . i.name)
				# updateAllMetas()

# self.report({'ERROR'}, "My message")

def createSpeedMeta(selection):
	print("createSpeedMeta")

	context1 = bpy.context.area.type
	if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
		print("temporarily switching context where cursor is off of " + str(context1) + " to SEQUENCE***")
		bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at 		for 

	# if meta in selected
	metastrips = [my_strip for my_strip in selection if my_strip.type == 'META' and my_strip.name.find("meta_") != -1]
	if len(metastrips) > 0:
		for win in bpy.data.window_managers[0].windows:
			for area in [area for area in win.screen.areas if area.type=="SEQUENCE_EDITOR"]:
				context = [region for region in area.regions if region.type=="WINDOW"][0]	# FIXME: context doesn't have a default value
				print(context)
		context = {'window': bpy.context.window, 'screen': screen, 'area': area, 'region': region, 'scene': bpy.context.scene}
		context1 = bpy.context.area.type
		if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
			print("temporarily switching context where cursor is off of " + str(context1) + " to SEQUENCE***")
			bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at 		for my_meta_strip in metastrips:
		for my_meta_strip in metastrips:
			if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
				print("temporarily switching context where cursor is off of " + str(context1) + " to SEQUENCE***")
				bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at 		for 
			print("--- opening " + my_meta_strip.name)
			#context.action='DESELECT'
			bpy.ops.sequencer.select_all(context, action='DESELECT')	# FIXME need context override
			my_meta_strip.select = True
			bpy.ops.sequencer.meta_toggle(context)
			my_meta_strip.select = False
			bpy.ops.sequencer.select_all(bpy.ops.sequencer.select_all, action='SELECT')
			print("should be inside meta with first non-meta strip (" + bpy.context.selected_sequences[0].name + ")")
			createSpeedMeta(bpy.context.selected_sequences)   # fixme

			bpy.ops.sequencer.select_all(action='SELECT')
			speedstrips = [my_strip for my_strip in bpy.context.selected_sequences if my_strip.type == 'SPEED' and my_strip.name.find("speed_") != -1]
			if len(speedstrips) > 0:
				frames = speedstrips[0].frame_final_duration
				print("will set meta frame number to " + str(frames))
			print("--- closing meta" + my_meta_strip.name)
			bpy.ops.sequencer.select_all(action='DESELECT')
			my_meta_strip.select = True
			bpy.ops.sequencer.meta_toggle()
			bpy.context.selected_sequences[0].frame_final_duration = frames
			#return

		bpy.context.area.type = context1
	#else: # if video in selected


	print(" done with meta's.  On to movie clips")

	speedstrips = [my_strip for my_strip in selection if my_strip.type == 'SPEED' and my_strip.name.find("speed_") != -1]
	not_had_speed = len(speedstrips) == 0 and True or False
	if not_had_speed:
		print(" no speed")
	else:
		bpy.ops.sequencer.select_all(action='DESELECT')
		for my_strip in speedstrips:
			print(" removing " + my_strip.name)
			my_strip.select = True
		bpy.ops.sequencer.delete()

	bpy.ops.sequencer.select_all(action='DESELECT')

	strips_movie = [my_strip for my_strip in selection if my_strip.type == 'MOVIE']
	if len(strips_movie) == 0:
		print("no MOVIE strips at this level")
	else:
		if True: # TODO check to see if exiftool available
			# get exiftool metadata
			et = exiftool.ExifTool()
			if et.running == False:
				et.start()

		# step 1a --- EXIF
		fps_scene = bpy.context.scene.render.fps

		for this_movie in strips_movie:
			# step 1 --- EXIF lookup and get speed multiplier

			print(" MOVIE " + this_movie.name + " " + bpy.path.abspath(this_movie.filepath))
			exif_metadata = et.get_metadata_batch([bpy.path.abspath(this_movie.filepath)])

			d = exif_metadata[0]

			# step 1b --- speed adjustment
			fps_this = d[[x for x in d if "FrameRate" in x][0]]
			duration_sec = d[[x for x in d if "Duration" in x][0]]	# FIXME: strip might be cut already, so duration could be different than overall source clip duration

			speed_ratio = fps_scene / fps_this
			frames = fps_this * duration_sec * speed_ratio
			print(" " + str(round(fps_scene, 2)) + " / " + str(round(fps_this, 2)) + " fps = speed ratio = " + str(round(speed_ratio, 2)))
			print(" duration=" + str(int(duration_sec)) + " secs, frames=" + str(int(frames)))

			# --- assign values
			# speed_length = length - not needed since length adjusts to video length, adjust
			this_movie.frame_final_duration = frames

			# --- step 2 make speed filter
			bpy.ops.sequencer.select_all(action='SELECT')
			effect_speed_this_movie = [my_strip for my_strip in bpy.context.selected_sequences if my_strip.type == 'SPEED' and my_strip.name.find("speed_") != -1]
			if len(effect_speed_this_movie) == 0:
				print(" adding speed with " + bpy.path.abspath(this_movie.filepath))
				bpy.ops.sequencer.select_all(action='DESELECT')
				this_movie.select = True
				# note that the newly made effect strip will be selected, so we don't have to add it to "selection"

				context1 = bpy.context.area.type
				if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
					print("temporarily switching context where cursor is off of " + str(context1) + " to SEQUENCE***")
					bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at https://www.blender.org/api/blender_python_api_2_77_release/bpy.ops.html for alternative

				print("should have " + this_movie.name)
				print(bpy.context.selected_sequences)	# NOTE: [bpy.data.scenes['Scene'].sequence_editor.sequences_all["0001-0283.001"]]
				bpy.ops.sequencer.effect_strip_add(filepath=bpy.path.abspath(this_movie.filepath), type='SPEED')	# fixme this needs poll
				bpy.context.selected_sequences[0].name = "speed_" + str(this_movie.name)
				bpy.context.area.type = context1
			else:
				#effect_speed[0]	# TODO:
				print("*** found speed assigned to this movie")

		# step 3 make meta
		if len(strips_movie) > 0 and not_had_speed:
			if not_had_speed:
				print("clips not in meta, so making one")
				metastrips = [my_strip for my_strip in selection if my_strip.type != 'META']
				bpy.ops.sequencer.select_all(action='DESELECT')
				for my_strip in metastrips:
					my_strip.select = True
					print(my_strip.type + " " + my_strip.name)
					# Note: can't make meta without adding the created speed effect also
					if my_strip.type == "MOVIE":
						strips_movie = [my_strip for my_strip in bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences_all if my_strip.name == "speed_" + str(this_movie.name)]
						if len(strips_movie) > 0:
							bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences_all["speed_" + str(this_movie.name)].select = True
							print("found speed_" + str(this_movie.name))
						else:
							print("couldn't find speed effect for movie speed_" + str(this_movie.name))
			else:
				bpy.ops.sequencer.select_all(action='SELECT')
				metastrips = [my_strip for my_strip in selection if my_strip.type == 'META']
				for my_meta_strip in metastrips:
					my_meta_strip.select = False
			print("active strips")
			active_strips = bpy.context.selected_sequences
			if len(active_strips) > 0:
				for selected_strip in active_strips:
					print("selected " + selected_strip.name)
			else:
				print("no active strips")
			# for my_strip in selection:
				# print("adding " + my_strip.type + " " + my_strip.name + " to selections")
				# my_strip.select = True
			# for my_strip in selection:
				# my_strip.select = True
			bpy.ops.sequencer.meta_make()
			bpy.context.selected_sequences[0].name = "meta_" + str(this_movie.name) # TODO: verify name isn't already used
			bpy.context.selected_sequences[0].frame_final_duration = frames	#FIXME: frames might be out of sync for use here

		et.terminate()	# TODO make more efficient by leaving on or using different exiftool (probably from extra)

def updateAllMetas():
	# TODO: might have to go to top level of vse (exit out of a meta)
	bpy.ops.sequencer.select_all(action='SELECT')
	#bpy.ops.sequencerextra.select_all_by_type(type='META')
	metastrips = [my_strip for my_strip in bpy.context.sequences if my_strip.type == 'META' and my_strip.name.find("meta_") != -1]
	print("updateAllMetas with " + str(len(metastrips)) + " strips")
	createSpeedMeta(metastrips)

# Blender UI and app integration
def my_object_button_add(self, context):
	self.layout.operator(
		MovieTimeToFPS.bl_idname,
		text="Selected Movie Time to FPS meta",
		icon='PLUGIN')
	self.layout.separator()


# This allows you to right click on a button and link to the manual
def my_object_manual_add():
	url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
	url_manual_mapping = (
		("bpy.ops.mesh.add_object", "Modeling/Objects"),
		)
	return url_manual_prefix, url_manual_mapping

# registeration
def register():
	bpy.utils.register_class(VSEtoFPSPanel)
	bpy.utils.register_class(MovieTimeToFPS)
	bpy.utils.register_manual_map(my_object_manual_add)
	bpy.types.SEQUENCER_MT_strip.prepend(my_object_button_add)

def unregister():
	bpy.utils.unregister_class(VSEtoFPSPanel)
	bpy.utils.unregister_class(MovieTimeToFPS)
	bpy.utils.unregister_manual_map(my_object_manual_add)
	bpy.types.SEQUENCER_MT_strip.remove(my_object_button_add)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
