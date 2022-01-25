from secml_malware.attack.blackbox.c_black_box_format_exploit_evasion import CBlackBoxFormatExploitEvasionProblem
from secml_malware.attack.blackbox.c_black_box_padding_evasion import CBlackBoxPaddingEvasionProblem
from secml_malware.attack.blackbox.c_blackbox_header_problem import CBlackBoxHeaderEvasionProblem
from secml_malware.attack.blackbox.c_blackbox_headerfields_problem import CBlackBoxHeaderFieldsEvasionProblem
from secml_malware.attack.blackbox.c_gamma_evasion import CGammaEvasionProblem
from secml_malware.attack.blackbox.c_gamma_sections_evasion import CGammaSectionsEvasionProblem
from secml_malware.attack.blackbox.c_wrapper_phi import CEmberWrapperPhi, CEnd2EndWrapperPhi, CSorelWrapperPhi
from secml_malware.attack.whitebox import CHeaderEvasion, CExtendDOSEvasion, \
	CContentShiftingEvasion, CPaddingEvasion
from secml_malware.attack.whitebox.c_headerfields_evasion import CHeaderFieldsEvasion
from secml_malware.models import CClassifierEmber, CClassifierEnd2EndMalware
from secml_malware.models.c_classifier_sorel_net import CClassifierSorel

from constants import *
from prompts import error_prompt, crash_prompt
from state import global_state


def create_correct_whitebox_attack(args):
	is_debug = False  # bool(args.is_debug)
	threshold = float(args.threshold)
	iterations = int(args.iterations)
	net = args.net
	chunk = int(args.chunk) if args.chunk is not None else None

	to_inject = int(args.inject)

	if args.type == FULL_DOS:
		attack = CHeaderEvasion(
			net,
			is_debug=is_debug,
			random_init=False,
			iterations=iterations,
			optimize_all_dos=True,
			threshold=threshold
		)
	elif args.type == EXTEND:
		attack = CExtendDOSEvasion(
			net,
			pe_header_extension=to_inject,
			iterations=iterations,
			is_debug=is_debug,
			threshold=threshold,
			random_init=False,
			chunk_hyper_parameter=int(chunk) if chunk else None
		)
	elif args.type == SHIFT:
		attack = CContentShiftingEvasion(
			net,
			preferable_extension_amount=to_inject,
			iterations=iterations,
			is_debug=is_debug,
			threshold=threshold,
			random_init=False,
			chunk_hyper_parameter=chunk
		)
	elif args.type == PADDING:
		attack = CPaddingEvasion(
			net,
			is_debug=is_debug,
			random_init=True,
			iterations=iterations,
			how_many=to_inject,
			threshold=threshold
		)
	elif args.type == PARTIAL_DOS:
		attack = CHeaderEvasion(
			net,
			is_debug=is_debug,
			random_init=True,
			iterations=iterations,
			optimize_all_dos=False,
			threshold=threshold
		)
	elif args.type == HEADER_FIELDS:
		attack = CHeaderFieldsEvasion(
			net,
			is_debug=is_debug,
			random_init=True,
			iterations=iterations,
			threshold=threshold
		)
	else:
		raise NotImplementedError(f'{args.type} not implemented yet')
	return attack


def create_gamma_black_box_attack(cli_args):
	how_many_sections = int(cli_args.inject)
	cache_file = cli_args.cache_file
	population_size = int(cli_args.population_size)
	iterations = int(cli_args.query_budget) // population_size + 1
	penalty_regularizer = float(cli_args.reg_par)
	goodware_folder = cli_args.goodware_folder
	threshold = float(cli_args.threshold)
	section_to_extract = ['.rdata']
	if cli_args.type == GAMMA_PADDING:
		section_population, what_from_who = CGammaEvasionProblem.create_section_population_from_folder(
			goodware_folder, how_many_sections, sections_to_extract=section_to_extract, cache_file=cache_file)
		problem = CGammaEvasionProblem(section_population,
									   cli_args.model,
									   penalty_regularizer=penalty_regularizer,
									   population_size=population_size,
									   iterations=iterations,
									   threshold=threshold)
	elif cli_args.type == GAMMA_SECTIONS:
		section_population, what_from_who = CGammaSectionsEvasionProblem.create_section_population_from_folder(
			goodware_folder, how_many_sections, sections_to_extract=section_to_extract, cache_file=cache_file)
		problem = CGammaSectionsEvasionProblem(section_population,
											   cli_args.model,
											   penalty_regularizer=penalty_regularizer,
											   population_size=population_size,
											   iterations=iterations,
											   threshold=threshold)
	else:
		raise NotImplementedError(f'{cli_args.type} not implemented yet')
	return problem


def create_byte_based_black_box_attack(cli_args):
	population_size = int(cli_args.population_size)
	inject = int(cli_args.inject)
	iterations = int(cli_args.query_budget) // population_size + 1
	model = cli_args.model
	threshold = float(cli_args.threshold)
	if cli_args.type == SHIFT:
		problem = CBlackBoxFormatExploitEvasionProblem(model, preferable_extension_amount=inject, pe_header_extension=0,
													   iterations=iterations, population_size=population_size)
	elif cli_args.type == EXTEND:
		problem = CBlackBoxFormatExploitEvasionProblem(model, preferable_extension_amount=0, pe_header_extension=inject,
													   iterations=iterations, population_size=population_size)
	elif cli_args.type == PARTIAL_DOS:
		problem = CBlackBoxHeaderEvasionProblem(model, optimize_all_dos=False, iterations=iterations,
												population_size=population_size)
	elif cli_args.type == FULL_DOS:
		problem = CBlackBoxHeaderEvasionProblem(model, optimize_all_dos=True, iterations=iterations,
												population_size=population_size)
	elif cli_args.type == PADDING:
		problem = CBlackBoxPaddingEvasionProblem(model, how_many_padding_bytes=inject, iterations=iterations,
												 population_size=population_size)
	elif cli_args.type == HEADER_FIELDS:
		problem = CBlackBoxHeaderFieldsEvasionProblem(model, iterations=iterations,
												 population_size=population_size)
	else:
		raise KeyError(f"{cli_args.type} not recognized as attack")
	return problem


def create_wrapper_for_global_target():
	if type(global_state.target) == CClassifierEmber:
		return CEmberWrapperPhi(global_state.target)
	if type(global_state.target) == CClassifierEnd2EndMalware:
		return CEnd2EndWrapperPhi(global_state.target)
	if type(global_state.target) == CClassifierSorel:
		return CSorelWrapperPhi(global_state.target)
	if hasattr(global_state.target, 'load_wrapper'):
		try:
			return global_state.target.load_wrapper()
		except Exception as e:
			crash_prompt("Error in loading wrapper of plugin model!")
			crash_prompt(f"Exception was {e}")
			raise e
	error_prompt('Incorrect target')
	raise NotImplementedError('Incorrect target')
