from collections import OrderedDict
import pairoptions


def iccasmoptions(*args):
    """
    ICCASMOPTIONS - CG + ASM with sub-block ICC preconditioner

    Symmetric counterpart of iluasmoptions. Use this for symmetric
    positive-definite operators (e.g. SSA stressbalance, thermal
    diffusion). CG is the optimal Krylov method for SPD; ICC is the
    SPD analogue of ILU and gives the same fill-in/conditioning
    trade-off without breaking symmetry.

    PETSc's ICC is sequential, so we wrap it in ASM for parallel runs
    (parallel via block-Jacobi-style domain decomposition with an
    ICC sub-solve on each subdomain).

       Usage:
          options = iccasmoptions
    """

    options = pairoptions.pairoptions(*args)
    iccasm = OrderedDict()

    iccasm['toolkit'] = 'petsc'
    iccasm['mat_type'] = options.getfieldvalue('mat_type', 'aij')
    iccasm['ksp_type'] = options.getfieldvalue('ksp_type', 'cg')
    iccasm['pc_type'] = options.getfieldvalue('pc_type', 'asm')
    iccasm['sub_pc_type'] = options.getfieldvalue('sub_pc_type', 'icc')
    iccasm['pc_asm_overlap'] = options.getfieldvalue('pc_asm_overlap', 5)
    iccasm['ksp_max_it'] = options.getfieldvalue('ksp_max_it', 100)
    iccasm['ksp_rtol'] = options.getfieldvalue('ksp_rtol', 1e-8)

    return iccasm
