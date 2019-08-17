bl_info = {
	"name": "Meta Adjust Video Speed to Render",
	"author": "escapecode",
	"version": (2, 79, 2),
	"blender": (2, 79, 0),
	"category": "Sequencer",
	"location": "Sequencer > Strip, Render Panel",
	"description": "Adjust video clip's speed to match Render FPS",
	"warning": "Auto-make meta on new movie add not working yet",
	"wiki_url": "https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki",
	'tracker_url': 'https://github.com/escapecode/Blender-VSE_FPS_adjust/issues',
	'support': 'TESTING'
}

import bpy
import os, sys

try:
	import exiftool
except ImportError:
	print("\nExiftool is needed on your computer to use this add-on (e.g. apt-get install libimage-exiftool-perl_8.60-2), http://www.sno.phy.queensu.ca/~phil/exiftool/, https://smarnach.github.io/pyexiftool/ and rename to exiftool.exe or exiftool and put in C:\Windows or /usr/bin, etc. put exiftool.py in blender/2.7x/python/lib/ or other lib folder\n")
	sys.exit(0)

from bpy.types import Menu, Panel

icon_collections = {}

bpy.types.Scene.FPS_last = 0
bpy.types.Scene.prop_last_sequences_num = 0
bpy.types.Scene.prop_running = False

bpy.types.Scene.prop_bFPSsync = bpy.props.BoolProperty(
	name="Auto-adjust Metas to FPS",
	description="Automatically adjust associated VSE Meta speeds when Render FPS adjusted",
	default=False,
	# update=doPolling
)

bpy.types.Scene.prop_bfileAddMeta = bpy.props.BoolProperty(
	name="Auto make Meta when movie strip added",
	description="When new movie strips added to sequencer timeline, automatically turn them into a Meta",
	default=False,
	# update=doPolling
)

# ----- Classes and Functions

# Universally add this script's functionality to Blender (for use on menu entries, command search, buttons, etc.)
class SpeedMeta_OpCreate(bpy.types.Operator):
	"""Wrap selected strips in meta with movie strip speed adjusted to scene FPS"""	  # blender will use this text as a tooltip for menu items and buttons (which is not language normalized)
	bl_idname = "sequencer.metafromfpscreate"		# unique identifier for buttons and menu items to reference.
	bl_label = "Make Speed Meta to FPS Render"		 # display name in the interface.
	bl_space_type = "SEQUENCE_EDITOR"
	bl_region_type = 'WINDOW'
	#bl_context = "object"
	#bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

	def execute(self, context):		# execute() is called by blender when running the operator.
		print("SpeedMeta_OpCreate { executed }")
		speedMeta_meta_create(bpy.context.selected_sequences)

		return {'FINISHED'}			# this lets blender know the operator finished successfully.

class SpeedMeta_OpUpdate(bpy.types.Operator):
	"""Update selected strips in meta with movie strip speed adjusted to scene FPS"""	  # blender will use this text as a tooltip for menu items and buttons (which is not language normalized)
	bl_idname = "sequencer.metafromfpsupdate"		# unique identifier for buttons and menu items to reference.
	bl_label = "Update Speed to FPS Metas"		 # display name in the interface.
	bl_space_type = "SEQUENCE_EDITOR"
	bl_region_type = 'WINDOW'
	#bl_context = "object"
	#bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

	def execute(self, context):		# execute() is called by blender when running the operator.
		print("SpeedMeta_OpUpdate executed")
		speedMeta_metas_update()

		return {'FINISHED'}			# this lets blender know the operator finished successfully.

class SpeedMeta_UIPanel(bpy.types.Panel):
	"""Creates a new Panel in the Render properties tab"""
	bl_idname = "RENDER_PT_VSEtoFPS"
	bl_label = "VSE FPS sync"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"
	bl_options = {'DEFAULT_CLOSED'}

	def panelAdd(self, context):
		layout = self.layout
		row = layout.row()
		row.prop(bpy.context.scene, "prop_bFPSsync")

		row = layout.row()
		row.prop(bpy.context.scene, "prop_bfileAddMeta")

	def draw(self, context):
		row = self.layout.row()

		row.label(text="FPS: " + str(context.scene.render.fps), icon='WORLD_DATA')
		row.prop(bpy.context.scene, "prop_bFPSsync")

	def doPolling(self):
		# part 1 --- auto meta new movie strips
		if bpy.context.scene.prop_running == False and bpy.context.scene.prop_bfileAddMeta == True and len(bpy.context.sequences) > bpy.context.scene.prop_last_sequences_num:
			bpy.types.Scene.prop_running = True
			strips_movie = [my_strip for my_strip in bpy.context.selected_sequences if my_strip.type == 'MOVIE']
			if len(strips_movie) > 0:
				# if hasattr(bpy.context.scene.sequence_editor, "sequences"):
				print("create")
				bpy.ops.sequencer.metafromfpscreate('EXEC_DEFAULT')
				# speedMeta_meta_create(bpy.context.selected_sequences)

			bpy.types.Scene.prop_last_sequences_num = len(bpy.context.sequences)
			bpy.types.Scene.prop_running = False

		# part 2 --- auto update metas when render FPS changed
		if bpy.context.scene.prop_bFPSsync == True and (bpy.context.scene.render.fps / bpy.context.scene.render.fps_base) != bpy.types.Scene.FPS_last:
			print("\n**** Render FPS changed to " + str(bpy.context.scene.render.fps))
			bpy.types.Scene.FPS_last = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base

			if hasattr(bpy.context.scene.sequence_editor, "sequences"):
				bpy.ops.sequencer.metafromfpsupdate('EXEC_DEFAULT')
				# speedMeta_metas_update()

	bpy.types.Scene.FPS_last = 0
	# Add this property to the Render panel in the Dimensions tab
	bpy.types.RENDER_PT_dimensions.append(panelAdd)

	# ----- Main loop
	bpy.app.handlers.scene_update_post.append(doPolling)

class SpeedMeta_UIButton(bpy.types.Header):
	bl_space_type = 'SEQUENCE_EDITOR'

	vse_fpsmeta_buttons = bpy.utils.previews.new()
	vse_fpsmeta_buttons.load("iconSpeedMeta_create", os.path.join(os.path.dirname(__file__), "vse_fps_adjust.png"), 'IMAGE')

	icon_collections['main'] = vse_fpsmeta_buttons

	@classmethod
	def poll(self, context):
	   return

	def draw(self, context):
		layout = self.layout

		icons = icon_collections["main"]

		row = layout.row(1)
		row.operator("sequencer.metafromfpscreate",  text="", icon_value= icons.get("iconSpeedMeta_create").icon_id);


def speedMeta_meta_create(selection):
	print("speedMeta_meta_create")
	
	# TODO check to make sure exiftool works
	
	if (bpy.context.area is None):
		return	#	NOTE: This should be OK, since it prevents some events that shouldn't be processed (e.g. changing FPS, and then turning on auto adjust FPS)
	
	context1 = bpy.context.area.type
	context_orig = context1
	if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
		print("temporarily switching context cursor off of " + str(context1) + " to SEQUENCE***")
		bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at 		for 
	
	# if meta in selected
	metastrips = [my_strip for my_strip in selection if my_strip.type == 'META' and my_strip.name.find("meta_") != -1]
	if len(metastrips) > 0:
		for win in bpy.data.window_managers[0].windows:
			for area in [area for area in win.screen.areas if area.type=="SEQUENCE_EDITOR"]:
				region = [region for region in area.regions if region.type=="WINDOW"][0]	# FIXME: context doesn't have a default value
		context = {'window': bpy.context.window, 'screen': bpy.context.screen, 'area': area, 'region': region, 'scene': bpy.context.scene}
		if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
			print("temporarily switching context  cursor off of " + str(context1) + " to SEQUENCE***")
			bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at 		for my_meta_strip in metastrips:
		for my_meta_strip in metastrips:
			print("\n--- opening " + my_meta_strip.name)
			#context.action='DESELECT'
			bpy.ops.sequencer.select_all(context, action='DESELECT')	# FIXME need context override
			my_meta_strip.select = True
			bpy.ops.sequencer.meta_toggle(context)
			my_meta_strip.select = False
			bpy.ops.sequencer.select_all(action='SELECT')
			print("should be inside meta with first non-meta strip (" + bpy.context.selected_sequences[0].name + ")")
			speedMeta_meta_create(bpy.context.selected_sequences)   # fixme

			bpy.ops.sequencer.select_all(action='SELECT')
			speedstrips = [my_strip for my_strip in bpy.context.selected_sequences if my_strip.type == 'SPEED' and my_strip.name.find("speed_") != -1]
			if len(speedstrips) > 0:
				frames = speedstrips[0].frame_final_duration
				print("will set meta frame number to " + str(frames))
			print("--- closing " + my_meta_strip.name + "\n")
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
		fps_scene = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base

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
				print(" adding speed with " + this_movie.filepath)
				bpy.ops.sequencer.select_all(action='DESELECT')
				this_movie.select = True
				# note that the newly made effect strip will be selected, so we don't have to add it to "selection"

				context1 = bpy.context.area.type
				if context1 != 'SEQUENCE_EDITOR':	# NOTE: bpy.context.area.type = '?'
					print("temporarily switching context where cursor is off of " + str(context1) + " to SEQUENCE***")
					bpy.context.area.type = 'SEQUENCE_EDITOR'	# NOTE: see overrides at https://www.blender.org/api/blender_python_api_2_77_release/bpy.ops.html for alternative

				# print("should have " + this_movie.name)
				# print("should have " +this_movie.filepath)
				# print(bpy.context.selected_sequences)	# NOTE: [bpy.data.scenes['Scene'].sequence_editor.sequences_all["0001-0283.001"]]
				bpy.ops.sequencer.effect_strip_add(type='SPEED')	# fixme this needs poll
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
							# FIXME: some speed effect names are truncated based off of this_movie.name, and causes the effect not to be found
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

	if context_orig != 'SEQUENCE_EDITOR' and context_orig != '':
		print("switching context back to " + context_orig)
		bpy.context.area.type = context_orig

def speedMeta_metas_update():
	# TODO: might have to go to top level of vse (exit out of a meta)
	bpy.ops.sequencer.select_all(action='SELECT')
	#bpy.ops.sequencerextra.select_all_by_type(type='META')
	metastrips = [my_strip for my_strip in bpy.context.sequences if my_strip.type == 'META' and my_strip.name.find("meta_") != -1]
	print("speedMeta_metas_update using " + str(len(metastrips)) + " strips")
	speedMeta_meta_create(metastrips)

# Adds VSE > strip menu entry
def speedMeta_menuentry_add(self, context):
	self.layout.operator(
		SpeedMeta_OpCreate.bl_idname,
		text="Adjust Video's Speed to Render FPS via Meta",
		icon='PLUGIN'
	)
	self.layout.separator()

# Allows right click on a button and link to the manual
def speedMeta_manual_add():
	url_manual_prefix = "https://github.com/escapecode/Blender-VSE_FPS_adjust"
	url_manual_mapping = (
		("bpy.ops.mesh.add_object", "Modeling/Objects"),
	)
	return url_manual_prefix, url_manual_mapping

# ----- Registration and startup

def register():

	bpy.utils.register_class(SpeedMeta_OpCreate)
	bpy.utils.register_class(SpeedMeta_OpUpdate)
	bpy.utils.register_class(SpeedMeta_UIPanel)
	bpy.utils.register_manual_map(speedMeta_manual_add)
	bpy.types.SEQUENCER_MT_strip.prepend(speedMeta_menuentry_add)
	bpy.utils.register_class(SpeedMeta_UIButton)

def unregister():
	bpy.utils.unregister_class(SpeedMeta_OpCreate)
	bpy.utils.unregister_class(SpeedMeta_OpUpdate)
	bpy.utils.unregister_class(SpeedMeta_UIPanel)
	bpy.utils.unregister_manual_map(speedMeta_manual_add)
	bpy.types.SEQUENCER_MT_strip.remove(speedMeta_menuentry_add)

	for icon in icon_collections.values():
		bpy.utils.previews.remove(icon)
	icon_collections.clear()

	bpy.utils.unregister_class(SpeedMeta_UIButton)

# Allow running this script directly from Blender's text editor
# (to test the addon without having to install it)
if __name__ == "__main__":
	register()